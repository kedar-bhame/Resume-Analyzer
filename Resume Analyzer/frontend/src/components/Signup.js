import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [touched, setTouched] = useState({});
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const navigate = useNavigate();

  const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  
  const getPasswordStrength = (pwd) => {
    let strength = 0;
    if (pwd.length >= 6) strength++;
    if (pwd.length >= 8) strength++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++;
    if (/[0-9]/.test(pwd)) strength++;
    if (/[^a-zA-Z0-9]/.test(pwd)) strength++;
    return strength;
  };

  const getPasswordStrengthLabel = (strength) => {
    if (strength <= 1) return { label: 'Weak', color: '#ef4444', percent: 20 };
    if (strength <= 2) return { label: 'Fair', color: '#f97316', percent: 40 };
    if (strength <= 3) return { label: 'Good', color: '#eab308', percent: 60 };
    if (strength <= 4) return { label: 'Strong', color: '#84cc16', percent: 80 };
    return { label: 'Very Strong', color: '#22c55e', percent: 100 };
  };

  const passwordStrength = getPasswordStrength(password);
  const strengthInfo = getPasswordStrengthLabel(passwordStrength);

  const getFieldError = (field) => {
    if (!touched[field]) return '';
    if (field === 'name' && name && name.length < 2) return 'Name must be at least 2 characters';
    if (field === 'email' && email && !validateEmail(email)) return 'Invalid email address';
    if (field === 'password' && password && password.length < 6) return 'Password must be at least 6 characters';
    if (field === 'confirmPassword' && confirmPassword && password !== confirmPassword) return 'Passwords do not match';
    return '';
  };

  const handleBlur = (field) => {
    setTouched(prev => ({ ...prev, [field]: true }));
  };

  const isFormValid = 
    name && 
    email && 
    password && 
    confirmPassword && 
    validateEmail(email) && 
    password === confirmPassword && 
    password.length >= 6 && 
    agreedToTerms;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!isFormValid) {
      setError('Please fill in all fields correctly');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify({ name, email }));
        navigate('/');
      } else {
        setError(data.error || 'Signup failed');
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
        <div className="auth-box signup-slide-in">
          <div className="auth-header">
            <h2>Join Us Today</h2>
            <p className="auth-subtitle">Create your account to get started</p>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {/* Name Field */}
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <div className="input-wrapper">
                <span className="input-icon">👤</span>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => {
                    setName(e.target.value);
                    if (error) setError('');
                  }}
                  onBlur={() => handleBlur('name')}
                  placeholder="John Doe"
                  className={`form-input ${touched.name && getFieldError('name') ? 'error' : ''}`}
                />
                {name && name.length >= 2 && <span className="check-icon">✓</span>}
              </div>
              {touched.name && getFieldError('name') && (
                <span className="field-error">{getFieldError('name')}</span>
              )}
            </div>

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

              {/* Password Strength Meter */}
              {password && (
                <div className="password-strength">
                  <div className="strength-bar">
                    <div 
                      className="strength-fill" 
                      style={{
                        width: `${strengthInfo.percent}%`,
                        backgroundColor: strengthInfo.color,
                        transition: 'all 0.3s ease'
                      }}
                    ></div>
                  </div>
                  <span className="strength-label" style={{ color: strengthInfo.color }}>
                    Strength: {strengthInfo.label}
                  </span>
                </div>
              )}

              {/* Password Requirements */}
              {password && (
                <div className="password-requirements">
                  <p className="req-title">Password requirements:</p>
                  <ul>
                    <li className={password.length >= 6 ? 'met' : ''}>
                      {password.length >= 6 ? '✓' : '○'} At least 6 characters
                    </li>
                    <li className={/[a-z]/.test(password) && /[A-Z]/.test(password) ? 'met' : ''}>
                      {/[a-z]/.test(password) && /[A-Z]/.test(password) ? '✓' : '○'} Mix of uppercase & lowercase
                    </li>
                    <li className={/[0-9]/.test(password) ? 'met' : ''}>
                      {/[0-9]/.test(password) ? '✓' : '○'} Contains numbers
                    </li>
                    <li className={/[^a-zA-Z0-9]/.test(password) ? 'met' : ''}>
                      {/[^a-zA-Z0-9]/.test(password) ? '✓' : '○'} Contains special character
                    </li>
                  </ul>
                </div>
              )}

              {touched.password && getFieldError('password') && (
                <span className="field-error">{getFieldError('password')}</span>
              )}
            </div>

            {/* Confirm Password Field */}
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <div className="input-wrapper">
                <span className="input-icon">🔒</span>
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    if (error) setError('');
                  }}
                  onBlur={() => handleBlur('confirmPassword')}
                  placeholder="••••••••"
                  className={`form-input ${touched.confirmPassword && getFieldError('confirmPassword') ? 'error' : ''}`}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {touched.confirmPassword && getFieldError('confirmPassword') && (
                <span className="field-error">{getFieldError('confirmPassword')}</span>
              )}
            </div>

            {/* Terms & Conditions */}
            <div className="form-checkbox">
              <input
                id="agreeTerms"
                type="checkbox"
                checked={agreedToTerms}
                onChange={(e) => setAgreedToTerms(e.target.checked)}
              />
              <label htmlFor="agreeTerms">
                I agree to the <a href="#" className="auth-link">Terms & Conditions</a>
              </label>
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
                  Creating account...
                </>
              ) : (
                '🚀 Create Account'
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="auth-footer">
            <p>Already have an account? <Link to="/login" className="auth-link">Sign in here</Link></p>
          </div>
        </div>

        {/* Side Info */}
        <div className="auth-info">
          <div className="info-card">
            <h3>🎯 Get Started</h3>
            <ul>
              <li>Analyze your resume instantly</li>
              <li>Get ATS optimization tips</li>
              <li>Download professional templates</li>
              <li>Track improvements over time</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
