export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('Access-Control-Max-Age', '86400');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    // Get target URL from query parameter
    let targetUrl = req.query.url;
    
    if (!targetUrl) {
      return res.status(400).json({ error: 'No URL provided' });
    }

    // Don't auto-add https for URLs that explicitly start with http://
    if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
      targetUrl = 'https://' + targetUrl;
    }

    console.log('Proxying request to:', targetUrl);

    // Enhanced headers for DASH streaming
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'cross-site'
    };

    // Forward original headers that might be important
    if (req.headers.range) {
      headers['Range'] = req.headers.range;
    }
    if (req.headers.referer) {
      headers['Referer'] = req.headers.referer;
    }

    // Forward the request with timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch(targetUrl, {
      method: req.method,
      headers: headers,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
    }

    // Get content type and other important headers
    const contentType = response.headers.get('content-type') || 'application/octet-stream';
    const contentLength = response.headers.get('content-length');
    const acceptRanges = response.headers.get('accept-ranges');
    const contentRange = response.headers.get('content-range');
    
    // Set appropriate response headers
    res.setHeader('Content-Type', contentType);
    
    if (contentLength) {
      res.setHeader('Content-Length', contentLength);
    }
    if (acceptRanges) {
      res.setHeader('Accept-Ranges', acceptRanges);
    }
    if (contentRange) {
      res.setHeader('Content-Range', contentRange);
    }

    // For DASH streaming, we want to allow caching of segments but not the manifest
    if (targetUrl.includes('.mpd')) {
      // MPD manifest - no cache
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
      res.setHeader('Pragma', 'no-cache');
      res.setHeader('Expires', '0');
    } else {
      // Video segments - allow short-term caching
      res.setHeader('Cache-Control', 'public, max-age=60');
    }

    // Handle different response types
    if (response.status === 206) {
      // Partial content (range request)
      res.status(206);
    } else {
      res.status(response.status);
    }

    // Stream the response efficiently
    if (response.body) {
      // Use streaming for better performance
      const reader = response.body.getReader();
      
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          res.write(Buffer.from(value));
        }
        res.end();
      } catch (streamError) {
        console.error('Streaming error:', streamError);
        res.end();
      }
    } else {
      // Fallback for responses without body
      const buffer = await response.arrayBuffer();
      res.send(Buffer.from(buffer));
    }

  } catch (error) {
    console.error('Proxy error:', error);
    
    if (error.name === 'AbortError') {
      res.status(408).json({ 
        error: 'Request timeout', 
        details: 'The request took too long to complete' 
      });
    } else {
      res.status(500).json({ 
        error: 'Proxy request failed', 
        details: error.message,
        url: req.query.url
      });
    }
  }
}
