// Global viewer counter API endpoint
// This tracks viewers across all users in real-time

let globalViewers = new Map(); // In-memory storage (resets on deployment)
let totalCount = 0;

// Clean up expired sessions (older than 2 minutes)
function cleanupExpiredSessions() {
    const now = Date.now();
    const timeout = 120000; // 2 minutes
    
    for (const [sessionId, timestamp] of globalViewers.entries()) {
        if (now - timestamp > timeout) {
            globalViewers.delete(sessionId);
        }
    }
    
    totalCount = globalViewers.size;
}

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    try {
        const { action, sessionId } = req.method === 'POST' ? req.body : req.query;
        
        // Clean up expired sessions first
        cleanupExpiredSessions();
        
        switch (action) {
            case 'join':
                if (sessionId) {
                    globalViewers.set(sessionId, Date.now());
                    totalCount = globalViewers.size;
                    console.log(`Viewer joined: ${sessionId}, Total: ${totalCount}`);
                }
                break;
                
            case 'leave':
                if (sessionId && globalViewers.has(sessionId)) {
                    globalViewers.delete(sessionId);
                    totalCount = globalViewers.size;
                    console.log(`Viewer left: ${sessionId}, Total: ${totalCount}`);
                }
                break;
                
            case 'heartbeat':
                if (sessionId) {
                    globalViewers.set(sessionId, Date.now());
                    totalCount = globalViewers.size;
                }
                break;
                
            case 'get':
            default:
                // Just return current count
                break;
        }
        
        // Return current viewer count
        res.status(200).json({
            success: true,
            viewers: totalCount,
            timestamp: Date.now(),
            action: action || 'get'
        });
        
    } catch (error) {
        console.error('Viewer API error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error',
            viewers: 0
        });
    }
}
