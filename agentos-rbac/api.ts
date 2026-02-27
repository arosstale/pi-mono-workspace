import express, { Request, Response, NextFunction } from 'express';
import { 
  createUser, 
  getUserByEmail, 
  getUserById, 
  updateUserRole, 
  deactivateUser, 
  listUsers,
  verifyPassword,
  checkPermission,
  logAuditEvent,
  ROLES
} from './auth';
import { Pool } from 'pg';

const router = express.Router();
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Authentication middleware
async function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized', message: 'No token provided' });
  }
  
  // Verify token and get user
  const query = 'SELECT * FROM users WHERE id = (SELECT user_id FROM sessions WHERE token = $1 AND expires_at > NOW())';
  const result = await pool.query(query, [token]);
  
  if (!result.rows[0]) {
    return res.status(401).json({ error: 'Unauthorized', message: 'Invalid or expired token' });
  }
  
  req.user = result.rows[0];
  next();
}

// Authorization middleware
function requirePermission(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const { id: resourceId } = req.params;
    
    const hasPermission = await checkPermission(user.id, resource, action, resourceId);
    
    if (!hasPermission) {
      await logAuditEvent(
        user.id,
        `denied_${action}`,
        resource,
        resourceId,
        req.ip,
        req.headers['user-agent']
      );
      
      return res.status(403).json({
        error: 'Forbidden',
        message: `User lacks ${action} permission on ${resource}`
      });
    }
    
    await logAuditEvent(
      user.id,
      action,
      resource,
      resourceId,
      req.ip,
      req.headers['user-agent']
    );
    
    next();
  };
}

// POST /api/v1/users - Create user (admin only)
router.post('/users', 
  authenticate,
  requirePermission('user', 'create'),
  async (req: Request, res: Response) => {
    try {
      const { email, password, role, workspaceId } = req.body;
      
      if (!email || !password || !role || !workspaceId) {
        return res.status(400).json({ error: 'Bad Request', message: 'Missing required fields' });
      }
      
      if (!ROLES[role]) {
        return res.status(400).json({ error: 'Bad Request', message: 'Invalid role' });
      }
      
      const user = await createUser(email, password, role, workspaceId);
      
      res.status(201).json({
        id: user.id,
        email: user.email,
        role: user.role,
        workspaceId: user.workspaceId,
        createdAt: user.createdAt
      });
    } catch (error) {
      console.error('Error creating user:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to create user' });
    }
  }
);

// GET /api/v1/users - List users (admin only)
router.get('/users',
  authenticate,
  requirePermission('user', 'read'),
  async (req: Request, res: Response) => {
    try {
      const { workspaceId } = req.query;
      
      if (!workspaceId) {
        return res.status(400).json({ error: 'Bad Request', message: 'workspaceId required' });
      }
      
      const users = await listUsers(workspaceId as string);
      
      res.json(users.map(u => ({
        id: u.id,
        email: u.email,
        role: u.role,
        workspaceId: u.workspaceId,
        isActive: u.isActive,
        createdAt: u.createdAt,
        lastLogin: u.lastLogin
      })));
    } catch (error) {
      console.error('Error listing users:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to list users' });
    }
  }
);

// GET /api/v1/users/:id - Get user (self or admin)
router.get('/users/:id',
  authenticate,
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const currentUser = req.user;
      
      // Users can only read their own profile unless admin
      if (id !== currentUser.id && currentUser.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden', message: 'Can only read own profile' });
      }
      
      const user = await getUserById(id);
      
      if (!user) {
        return res.status(404).json({ error: 'Not Found', message: 'User not found' });
      }
      
      res.json({
        id: user.id,
        email: user.email,
        role: user.role,
        workspaceId: user.workspaceId,
        isActive: user.isActive,
        createdAt: user.createdAt,
        lastLogin: user.lastLogin
      });
    } catch (error) {
      console.error('Error getting user:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to get user' });
    }
  }
);

// PATCH /api/v1/users/:id/role - Update role (admin only)
router.patch('/users/:id/role',
  authenticate,
  requirePermission('user', 'update'),
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const { role } = req.body;
      
      if (!role || !ROLES[role]) {
        return res.status(400).json({ error: 'Bad Request', message: 'Invalid role' });
      }
      
      await updateUserRole(id, role);
      
      res.json({ message: 'Role updated successfully' });
    } catch (error) {
      console.error('Error updating role:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to update role' });
    }
  }
);

// DELETE /api/v1/users/:id - Deactivate user (admin only)
router.delete('/users/:id',
  authenticate,
  requirePermission('user', 'delete'),
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      
      await deactivateUser(id);
      
      res.json({ message: 'User deactivated successfully' });
    } catch (error) {
      console.error('Error deactivating user:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to deactivate user' });
    }
  }
);

// POST /api/v1/auth/login - Login
router.post('/auth/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({ error: 'Bad Request', message: 'Email and password required' });
    }
    
    const user = await getUserByEmail(email);
    
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized', message: 'Invalid credentials' });
    }
    
    const isValidPassword = verifyPassword(password, user.passwordHash);
    
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Unauthorized', message: 'Invalid credentials' });
    }
    
    // Create session token
    const token = require('crypto').randomBytes(32).toString('hex');
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7); // 7 days
    
    const query = `
      INSERT INTO sessions (id, user_id, token, expires_at, created_at)
      VALUES ($1, $2, $3, $4, NOW())
    `;
    await pool.query(query, [require('crypto').randomUUID(), user.id, token, expiresAt]);
    
    res.json({
      token,
      expiresAt,
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        workspaceId: user.workspaceId
      }
    });
  } catch (error) {
    console.error('Error logging in:', error);
    res.status(500).json({ error: 'Internal Server Error', message: 'Failed to login' });
  }
});

// GET /api/v1/permissions/check - Check permission
router.get('/permissions/check',
  authenticate,
  async (req: Request, res: Response) => {
    try {
      const { resource, action, resourceId } = req.query;
      
      if (!resource || !action) {
        return res.status(400).json({ error: 'Bad Request', message: 'Resource and action required' });
      }
      
      const hasPermission = await checkPermission(
        req.user.id,
        resource as string,
        action as string,
        resourceId as string
      );
      
      res.json({ hasPermission });
    } catch (error) {
      console.error('Error checking permission:', error);
      res.status(500).json({ error: 'Internal Server Error', message: 'Failed to check permission' });
    }
  }
);

export default router;