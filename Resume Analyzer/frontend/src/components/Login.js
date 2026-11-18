import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [touched, setTouched] = useState({});
  const navigate = useNavigate();

  const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  
  const isFormValid = email && password && validateEmail(email);
  
  const getFieldError = (field) => {
    if (!touched[field]) return '';
    if (field === 'email' && email && !validateEmail(email)) return 'Invalid email address';
    if (field === 'password' && password && password.length < 6) return 'Password must be at least 6 characters';
    return '';
  };

  const handleBlur = (field) => {
    setTouched(prev => ({ ...prev, [field]: true }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!isFormValid) {
      setError('Please fill in all fields correctly');
      return;
    }
    
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify({ name: data.name, email: data.email }));
        if (rememberMe) {
          localStorage.setItem('rememberMe', 'true');
          localStorage.setItem('savedEmail', email);
        }
        navigate('/');
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-wrapper">
      <div className="auth-container">
        <div className="auth-box login-slide-in">
          <div className="auth-header">
            <h2>Welcome Back</h2>
            <p className="auth-subtitle">Sign in to your account</p>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {/* Email Field */}
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <div className="input-wrapper">
                <span className="input-icon">📧</span>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (error) setError('');
                  }}
                  onBlur={() => handleBlur('email')}
                  placeholder="you@example.com"
                  className={`form-input ${touched.email && getFieldError('email') ? 'error' : ''}`}
                />
                {email && validateEmail(email) && <span className="check-icon">✓</span>}
              </div>
              {touched.email && getFieldError('email') && (
                <span className="field-error">{getFieldError('email')}</span>
              )}
            </div>

            {/* Password Field */}
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrapper">
                <span className="input-icon">🔐</span>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (error) setError('');
                  }}
                  onBlur={() => handleBlur('password')}
                  placeholder="••••••••"
                  className={`form-input ${touched.password && getFieldError('password') ? 'error' : ''}`}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {touched.password && getFieldError('password') && (
                <span className="field-error">{getFieldError('password')}</span>
              )}
            </div>

            {/* Remember Me */}
            <div className="form-checkbox">
              <input
                id="rememberMe"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
              />
              <label htmlFor="rememberMe">Remember me for next time</label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="btn primary submit-btn"
              disabled={loading || !isFormValid}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Signing in...
                </>
              ) : (
                '🚀 Sign In'
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="auth-footer">
            <p>Don't have an account? <Link to="/signup" className="auth-link">Sign up here</Link></p>
            <p><a href="#" className="auth-link">Forgot your password?</a></p>
          </div>
        </div>

        {/* Side Info */}
        <div className="auth-info">
          <div className="info-card">
            <h3>✨ Why Sign In?</h3>
            <ul>
              <li>Save your resume analysis history</li>
              <li>Get personalized recommendations</li>
              <li>Track your progress over time</li>
              <li>Access templates anytime</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
