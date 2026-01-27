
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, { name, phone, address });
      }
      navigate('/profile');
    } catch (error) {
      console.error('Authentication error:', error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page login-page">
      <div className="container">
        <div className="auth-container">
          <div className="auth-header">
            <h1>{isLogin ? 'Login' : 'Create Account'}</h1>
            <p>Welcome to Buroko's Kitchen</p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <>
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required={!isLogin}
                    placeholder="Enter your full name"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required={!isLogin}
                    placeholder="Enter your phone number"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="address">Delivery Address</label>
                  <textarea
                    id="address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    required={!isLogin}
                    placeholder="Enter your delivery address"
                    rows="3"
                  />
                </div>
              </>
            )}

            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Enter your email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
                minLength="6"
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Create Account')}
            </button>
          </form>

          <div className="auth-switch">
            <p>
              {isLogin ? "Don't have an account? " : 'Already have an account? '}
              <button
                type="button"
                className="link-btn"
                onClick={() => setIsLogin(!isLogin)}
              >
                {isLogin ? 'Sign up' : 'Login'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
