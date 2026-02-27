# AgentOS Phase 1: Multi-User Permissions

## Implementation Spec

**Goal:** Role-based access control for OpenClaw agents
**Timeline:** 30 days
**Deliverable:** Working RBAC system

---

## Data Model

```typescript
interface User {
  id: string;
  email: string;
  role: 'admin' | 'agent' | 'viewer';
  workspaceId: string;
  permissions: Permission[];
  createdAt: Date;
  lastLogin: Date;
}

interface Permission {
  resource: 'agent' | 'session' | 'skill' | 'config' | 'billing';
  action: 'create' | 'read' | 'update' | 'delete' | 'execute';
  conditions?: {
    ownOnly?: boolean;
    workspaceBound?: boolean;
  };
}

// Role definitions
const ROLES = {
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
```

---

## API Endpoints

```typescript
// User management
POST   /api/v1/users              // Create user (admin only)
GET    /api/v1/users              // List users (admin only)
GET    /api/v1/users/:id          // Get user (self or admin)
PATCH  /api/v1/users/:id          // Update user (self or admin)
DELETE /api/v1/users/:id          // Delete user (admin only)

// Role management
POST   /api/v1/users/:id/role     // Change role (admin only)

// Permission checks
GET    /api/v1/permissions/check  // Check if user can perform action

// Session ownership
GET    /api/v1/sessions           // List sessions (filtered by permissions)
```

---

## Middleware Implementation

```typescript
// Authorization middleware
function requirePermission(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const { agentId, sessionId } = req.params;
    
    // Check if user has permission
    const hasPermission = await checkPermission({
      userId: user.id,
      role: user.role,
      resource,
      action,
      resourceId: agentId || sessionId,
      workspaceId: user.workspaceId
    });
    
    if (!hasPermission) {
      return res.status(403).json({
        error: 'Forbidden',
        message: `User lacks ${action} permission on ${resource}`
      });
    }
    
    next();
  };
}

// Usage
app.post('/api/v1/agents', 
  authenticate, 
  requirePermission('agent', 'create'),
  createAgent
);

app.get('/api/v1/sessions/:id', 
  authenticate, 
  requirePermission('session', 'read'),
  getSession
);
```

---

## Database Schema

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'agent', 'viewer')),
  workspace_id UUID NOT NULL REFERENCES workspaces(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT true
);

-- Sessions table (with ownership)
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  workspace_id UUID NOT NULL REFERENCES workspaces(id),
  agent_id UUID REFERENCES agents(id),
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id UUID,
  workspace_id UUID,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_workspace_id ON sessions(workspace_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## CLI Commands

```bash
# User management
openclaw users create --email user@example.com --role agent
openclaw users list
openclaw users update-role user@example.com --role admin
openclaw users deactivate user@example.com

# Permission checks
openclaw permissions check --user user@example.com --resource agent --action create
```

---

## UI Changes

**Admin Dashboard:**
- User management table
- Role assignment dropdown
- Permission matrix view
- Audit log viewer

**Agent View:**
- Only own sessions visible
- Cannot see other users' agents
- Read-only on workspace skills

**Viewer View:**
- Read-only session list
- No agent creation
- No skill execution

---

## Testing Plan

```typescript
// Unit tests
describe('RBAC', () => {
  test('admin can create agents', () => {});
  test('agent can create own agents only', () => {});
  test('viewer cannot create agents', () => {});
  test('agent cannot delete other users agents', () => {});
  test('permissions are workspace-scoped', () => {});
});
```

---

## Migration Path

1. **Week 1:** Database schema + models
2. **Week 2:** API endpoints + middleware
3. **Week 3:** CLI commands + UI
4. **Week 4:** Testing + documentation

---

**Status:** Spec complete. Ready for implementation.

Platform Engineer Kelsey Hightowel
AgentOS Phase 1