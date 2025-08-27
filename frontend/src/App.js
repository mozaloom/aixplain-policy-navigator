import React, { useState } from 'react';
import axios from 'axios';
import { Search, FileText, CheckCircle, Scale } from 'lucide-react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/query', {
        query: query
      });
      setResults(response.data);
    } catch (err) {
      setError('Failed to process query. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };



  const getDisplayContent = (data) => {
    if (typeof data === 'string') return data;
    if (data?.output) return data.output;
    if (data?.message) return data.message;
    return 'Response received successfully';
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Policy Navigator</h1>
        <p>AI-powered government regulation search and compliance analysis</p>
      </div>

      <div className="search-container">
        <div className="input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="Ask about policies, executive orders, or compliance requirements..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
          />
          {query && (
            <button 
              className="clear-btn"
              onClick={() => setQuery('')}
              type="button"
            >
              ✕
            </button>
          )}
        </div>
        
        <div className="button-group">
          <button 
            className="btn btn-primary" 
            onClick={handleQuery}
            disabled={loading || !query.trim()}
          >
            <Search size={18} />
            Ask Policy Navigator
          </button>
        </div>

        {error && <div className="error">⚠️ {error}</div>}
        
        {!loading && !results && (
          <div className="examples">
            <h3>Try asking:</h3>
            <div className="example-queries">
              <button 
                className="example-btn"
                onClick={() => setQuery("Is Executive Order 14067 still in effect?")}
              >
                Is Executive Order 14067 still in effect?
              </button>
              <button 
                className="example-btn"
                onClick={() => setQuery("Has Section 230 been challenged in court?")}
              >
                Has Section 230 been challenged in court?
              </button>
              <button 
                className="example-btn"
                onClick={() => setQuery("What are compliance requirements for small businesses?")}
              >
                What are compliance requirements for small businesses?
              </button>
            </div>
          </div>
        )}
      </div>

      {(loading || results) && (
        <div className="results-container">
          {loading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Analyzing policies and regulations...</p>
            </div>
          ) : (
            <div>
              <div className="result-header">
                <FileText size={24} color="#3b82f6" />
                <h3 className="result-title">Analysis Results</h3>
              </div>
              <div className="result-content">
                {getDisplayContent(results).split('\n').map((line, index) => (
                  <p key={index} style={{marginBottom: line.startsWith('Source:') ? '0' : '12px', fontWeight: line.startsWith('Source:') ? '600' : 'normal', color: line.startsWith('Source:') ? '#3b82f6' : 'inherit'}}>
                    {line}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className="footer">
        <img 
          src="/powered_by_cirrusgo.png" 
          alt="Powered by CirrusGo" 
          className="powered-by"
          width="350"
          height="73"
        />
      </div>
    </div>
  );
}

export default App;