import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Tab,
  Tabs,
  Alert,
  CircularProgress
} from '@mui/material';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const { login, signup, forgotPassword } = useAuth();
  const navigate = useNavigate();

  const loginForm = useForm();
  const signupForm = useForm();
  const forgotPasswordForm = useForm();

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    setError('');
    setSuccess('');
  };

  const onLogin = async (data) => {
    setLoading(true);
    setError('');
    try {
      await login(data);
      navigate('/main');
    } catch (error) {
      setError(error.response?.data?.detail || 'Login failed');
    }
    setLoading(false);
  };

  const onSignup = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await signup(data);
      setTabValue(0);
      setSuccess('Account created successfully! Please login.');
    } catch (error) {
      setError(error.response?.data?.detail || 'Signup failed');
    }
    setLoading(false);
  };

  const onForgotPassword = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await forgotPassword(data.email);
      setSuccess('Password reset link has been sent to your email!');
      forgotPasswordForm.reset();
    } catch (error) {
      setError('Failed to send password reset email');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography variant="h4" align="center" gutterBottom>
            StudentConnect
          </Typography>
          
          <Tabs value={tabValue} onChange={handleTabChange} centered>
            <Tab label="Login" />
            <Tab label="Sign Up" />
            <Tab label="Forgot Password" />
          </Tabs>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}

          {tabValue === 0 && (
            <Box component="form" onSubmit={loginForm.handleSubmit(onLogin)} sx={{ mt: 3 }}>
              <TextField
                fullWidth
                label="Email"
                type="email"
                margin="normal"
                {...loginForm.register('email', { required: 'Email is required' })}
                error={!!loginForm.formState.errors.email}
                helperText={loginForm.formState.errors.email?.message}
              />
              <TextField
                fullWidth
                label="Password"
                type="password"
                margin="normal"
                {...loginForm.register('password', { required: 'Password is required' })}
                error={!!loginForm.formState.errors.password}
                helperText={loginForm.formState.errors.password?.message}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Login'}
              </Button>
              <Button
                fullWidth
                variant="text"
                onClick={() => setTabValue(2)}
                sx={{ mt: 1 }}
              >
                Forgot Password?
              </Button>
            </Box>
          )}

          {tabValue === 1 && (
            <Box component="form" onSubmit={signupForm.handleSubmit(onSignup)} sx={{ mt: 3 }}>
              <TextField
                fullWidth
                label="Name"
                margin="normal"
                {...signupForm.register('name', { required: 'Name is required' })}
                error={!!signupForm.formState.errors.name}
                helperText={signupForm.formState.errors.name?.message}
              />
              <TextField
                fullWidth
                label="Username"
                margin="normal"
                {...signupForm.register('username', { required: 'Username is required' })}
                error={!!signupForm.formState.errors.username}
                helperText={signupForm.formState.errors.username?.message}
              />
              <TextField
                fullWidth
                label="Email"
                type="email"
                margin="normal"
                {...signupForm.register('email', { required: 'Email is required' })}
                error={!!signupForm.formState.errors.email}
                helperText={signupForm.formState.errors.email?.message}
              />
              <TextField
                fullWidth
                label="Bio (optional)"
                margin="normal"
                multiline
                rows={2}
                {...signupForm.register('bio')}
              />
              <TextField
                fullWidth
                label="Password"
                type="password"
                margin="normal"
                {...signupForm.register('password', { 
                  required: 'Password is required',
                  minLength: { value: 6, message: 'Password must be at least 6 characters' }
                })}
                error={!!signupForm.formState.errors.password}
                helperText={signupForm.formState.errors.password?.message}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Sign Up'}
              </Button>
            </Box>
          )}

          {tabValue === 2 && (
            <Box component="form" onSubmit={forgotPasswordForm.handleSubmit(onForgotPassword)} sx={{ mt: 3 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Enter your email address and we'll send you a link to reset your password.
              </Typography>
              <TextField
                fullWidth
                label="Email"
                type="email"
                margin="normal"
                {...forgotPasswordForm.register('email', { required: 'Email is required' })}
                error={!!forgotPasswordForm.formState.errors.email}
                helperText={forgotPasswordForm.formState.errors.email?.message}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Send Reset Link'}
              </Button>
              <Button
                fullWidth
                variant="text"
                onClick={() => setTabValue(0)}
                sx={{ mt: 1 }}
              >
                Back to Login
              </Button>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;
