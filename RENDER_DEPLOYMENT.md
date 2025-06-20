# Render.com Configuration

This document explains how to deploy the Local RAG system to Render.com

## Important Note About Ollama

⚠️ **Limitation**: This deployment will NOT include Ollama models due to Render's resource constraints. The deployment will:
- Provide the Gradio UI interface
- Offer API endpoints
- Support OpenAI integration (if API key provided)
- Use basic text similarity for local queries (without heavy ML models)

For full local model functionality, run the system locally with Ollama installed.

## Deployment Steps

### 1. Prepare Your Repository

Ensure these files are in your repository:
- `fastapi_app.py` - Main application file
- `gradio_ui.py` - Gradio interface
- `requirements_deploy.txt` - Deployment dependencies
- `build.sh` - Build script
- `rag_file_loader.py` - RAG functionality
- `data/` directory with sample documents

### 2. Create Render Web Service

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `local-rag-system` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `python fastapi_app.py`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (deploys on git push)

### 3. Environment Variables

Add these environment variables in Render dashboard:

**Required:**
- `PORT`: `10000` (automatically set by Render)

**Optional:**
- `OPENAI_API_KEY`: Your OpenAI API key (for comparison features)

### 4. Resource Configuration

**Free Tier Limitations:**
- 512 MB RAM
- 0.1 CPU
- Sleeps after 15 minutes of inactivity
- 750 hours/month

**Paid Tier Recommendations:**
- **Starter**: $7/month - 512 MB RAM, 0.5 CPU
- **Standard**: $25/month - 2 GB RAM, 1 CPU (recommended)

## Deployment Commands

### Local Testing
```bash
# Install deployment dependencies
pip install -r requirements_deploy.txt

# Test the FastAPI app locally
python fastapi_app.py

# Test Gradio UI separately
python gradio_ui.py
```

### Build Script
The `build.sh` script will:
1. Install Python dependencies
2. Create data directory
3. Add sample documents
4. Set up the environment

## Post-Deployment

### 1. Access Your Application
- **Main UI**: `https://your-app-name.onrender.com/`
- **API Docs**: `https://your-app-name.onrender.com/api/docs`
- **Health Check**: `https://your-app-name.onrender.com/api/health`

### 2. Upload Your Documents
Since Render doesn't have persistent storage, you'll need to:
- Include documents in your git repository under `data/`
- Or use external storage (S3, Google Drive, etc.)

### 3. Monitor Performance
- Check Render dashboard for logs and metrics
- Monitor response times and memory usage
- Scale up if needed

## Limitations and Workarounds

### 1. No Ollama Models
**Problem**: Render can't run Ollama with large models
**Workaround**: 
- Use OpenAI API for cloud-based responses
- Implement basic text similarity for local queries
- Consider using Hugging Face Inference API for alternatives

### 2. No Persistent Storage
**Problem**: Files uploaded via UI won't persist
**Workaround**:
- Include documents in git repository
- Use external storage services
- Implement cloud storage integration

### 3. Cold Starts
**Problem**: Free tier sleeps after inactivity
**Workaround**:
- Upgrade to paid tier
- Use uptime monitoring services
- Accept slower first response

## Alternative Deployment Options

### 1. Railway
- Similar to Render
- Better resource allocation
- Persistent storage options

### 2. Google Cloud Run
- Pay-per-use pricing
- Better for larger models
- More configuration options

### 3. AWS Lambda + API Gateway
- Serverless deployment
- Good for API-only usage
- Requires more setup

### 4. DigitalOcean App Platform
- Good middle ground
- Competitive pricing
- Decent resource limits

## Production Considerations

### 1. Security
- Set up proper CORS policies
- Use HTTPS (Render provides this)
- Validate all inputs
- Rate limiting for API endpoints

### 2. Performance
- Implement caching for frequent queries
- Optimize document loading
- Monitor response times
- Consider CDN for static assets

### 3. Monitoring
- Set up health checks
- Monitor error rates
- Track user analytics
- Set up alerts for downtime

## Cost Estimation

### Render Pricing
- **Free**: $0/month (with limitations)
- **Starter**: $7/month (basic production)
- **Standard**: $25/month (recommended)
- **Pro**: $85/month (high performance)

### Additional Costs
- **OpenAI API**: Pay-per-use (~$0.002/1K tokens)
- **Custom Domain**: Free with paid plans
- **SSL Certificate**: Included

## Support and Troubleshooting

### Common Issues
1. **Build Failures**: Check `build.sh` permissions and dependencies
2. **Import Errors**: Ensure all files are in repository
3. **Memory Issues**: Upgrade to higher tier or optimize code
4. **Slow Responses**: Check for blocking operations

### Getting Help
- Render documentation: https://render.com/docs
- Check deployment logs in Render dashboard
- Monitor application logs for errors
- Use health check endpoint for diagnostics

## Conclusion

While the deployed version won't have full Ollama functionality, it provides:
- ✅ Web interface for document queries
- ✅ API endpoints for integration
- ✅ OpenAI comparison features
- ✅ Basic RAG functionality
- ✅ Easy sharing and collaboration

For full local model capabilities, continue using the system locally with Ollama installed.
