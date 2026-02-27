import { v4 as uuidv4 } from 'uuid';
import { createHash, randomBytes } from 'crypto';
import { Pool } from 'pg';

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Role definitions
export const ROLES = {
  admin: {
    description: 'Full workspace control',
    permissions: [
      { resource: 'agent', action: 'create' },
      { resource: 'agent', action: 'read' },
      { resource: 'agent', action: 'update' },
      { resource: 'agent', action: 'delete' },
      { resource: 'session', action: 'create' },
      { resource: 'session', action: 'read' },
      { resource: 'session', action: 'update' },
      { resource: 'session', action: 'delete' },
      { resource: 'skill', action: 'create' },
      { resource: 'skill', action: 'read' },
      { resource: 'skill', action: 'update' },
      { resource: 'skill', action: 'delete' },
      { resource: 'config', action: 'read' },
      { resource: 'config', action: 'update' },
      { resource: 'billing', action: 'read' },
      { resource: 'billing', action: 'update' },
    ]
  },
  agent: {
    description: 'Can run agents, manage own sessions',
    permissions: [
      { resource: 'agent', action: 'create' },
      { resource: 'agent', action: 'read', conditions: { ownOnly: true } },
      { resource: 'agent', action: 'update', conditions: { ownOnly: true } },
      { resource: 'agent', action: 'delete', conditions: { ownOnly: true } },
      { resource: 'session', action: 'create' },
      { resource: 'session', action: 'read', conditions: { ownOnly: true } },
      { resource: 'session', action: 'update', conditions: { ownOnly: true } },
      { resource: 'skill', action: 'read' },
      { resource: 'skill', action: 'execute' },
      { resource: 'config', action: 'read' },
    ]
  },
  viewer: {
    description: 'Read-only access to sessions',
    permissions: [
      { resource: 'agent', action: 'read', conditions: { workspaceBound: true } },
      { resource: 'session', action: 'read', conditions: { workspaceBound: true } },
      { resource: 'skill', action: 'read' },
    ]
  }
};

export interface User {
  id: string;
  email: string;
  passwordHash: string;
  role: 'admin' | 'agent' | 'viewer';
  workspaceId: string;
  isActive: boolean;
  createdAt: Date;
  lastLogin?: Date;
}

export interface Permission {
  resource: 'agent' | 'session' | 'skill' | 'config' | 'billing';
  action: 'create' | 'read' | 'update' | 'delete' | 'execute';
  conditions?: {
    ownOnly?: boolean;
    workspaceBound?: boolean;
  };
}

// Hash password
export function hashPassword(password: string): string {
  const salt = randomBytes(16).toString('hex');
  const hash = createHash('sha256')
    .update(password + salt)
    .digest('hex');
  return `${salt}:${hash}`;
}

// Verify password
export function verifyPassword(password: string, hashedPassword: string): boolean {
  const [salt, hash] = hashedPassword.split(':');
  const computedHash = createHash('sha256')
    .update(password + salt)
    .digest('hex');
  return hash === computedHash;
}

// Create user
export async function createUser(
  email: string,
  password: string,
  role: 'admin' | 'agent' | 'viewer',
  workspaceId: string
): Promise<User> {
  const id = uuidv4();
  const passwordHash = hashPassword(password);
  
  const query = `
    INSERT INTO users (id, email, password_hash, role, workspace_id, is_active, created_at)
    VALUES ($1, $2, $3, $4, $5, true, NOW())
    RETURNING *
  `;
  
  const result = await pool.query(query, [id, email, passwordHash, role, workspaceId]);
  return result.rows[0];
}

// Get user by email
export async function getUserByEmail(email: string): Promise<User | null> {
  const query = 'SELECT * FROM users WHERE email = $1 AND is_active = true';
  const result = await pool.query(query, [email]);
  return result.rows[0] || null;
}

// Get user by ID
export async function getUserById(id: string): Promise<User | null> {
  const query = 'SELECT * FROM users WHERE id = $1 AND is_active = true';
  const result = await pool.query(query, [id]);
  return result.rows[0] || null;
}

// Update user role
export async function updateUserRole(
  userId: string,
  newRole: 'admin' | 'agent' | 'viewer'
): Promise<void> {
  const query = 'UPDATE users SET role = $1 WHERE id = $2';
  await pool.query(query, [newRole, userId]);
}

// Deactivate user
export async function deactivateUser(userId: string): Promise<void> {
  const query = 'UPDATE users SET is_active = false WHERE id = $1';
  await pool.query(query, [userId]);
}

// List users in workspace
export async function listUsers(workspaceId: string): Promise<User[]> {
  const query = 'SELECT * FROM users WHERE workspace_id = $1 AND is_active = true';
  const result = await pool.query(query, [workspaceId]);
  return result.rows;
}

// Check permission
export async function checkPermission(
  userId: string,
  resource: string,
  action: string,
  resourceId?: string
): Promise<boolean> {
  const user = await getUserById(userId);
  if (!user) return false;
  
  const role = ROLES[user.role];
  if (!role) return false;
  
  // Check if user has permission
  const hasPermission = role.permissions.some(p => 
    p.resource === resource && p.action === action
  );
  
  if (!hasPermission) return false;
  
  // Check conditions (ownOnly, workspaceBound)
  const permission = role.permissions.find(p => 
    p.resource === resource && p.action === action
  );
  
  if (permission?.conditions?.ownOnly && resourceId) {
    // Check if resource belongs to user
    const query = `SELECT user_id FROM ${resource}s WHERE id = $1`;
    const result = await pool.query(query, [resourceId]);
    if (result.rows[0]?.user_id !== userId) return false;
  }
  
  return true;
}

// Log audit event
export async function logAuditEvent(
  userId: string,
  action: string,
  resourceType: string,
  resourceId?: string,
  ipAddress?: string,
  userAgent?: string
): Promise<void> {
  const query = `
    INSERT INTO audit_logs (user_id, action, resource_type, resource_id, ip_address, user_agent, created_at)
    VALUES ($1, $2, $3, $4, $5, $6, NOW())
  `;
  await pool.query(query, [userId, action, resourceType, resourceId, ipAddress, userAgent]);
}