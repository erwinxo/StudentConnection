import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const response = await authAPI.getCurrentUser();
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem('token');
    }
    setLoading(false);
  };

  const login = async (credentials) => {
    const response = await authAPI.login(credentials);
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    await fetchCurrentUser();
    return response.data;
  };

  const signup = async (userData) => {
    const response = await authAPI.signup(userData);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updateProfile = async (userData) => {
    const response = await authAPI.updateProfile(userData);
    setUser(response.data);
    return response.data;
  };

  const updateProfilePicture = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await authAPI.updateProfilePicture(formData);
    setUser(response.data);
    return response.data;
  };

  const forgotPassword = async (email) => {
    const response = await authAPI.forgotPassword(email);
    return response.data;
  };

  const resetPassword = async (token, newPassword) => {
    const response = await authAPI.resetPassword(token, newPassword);
    return response.data;
  };

  const value = {
    user,
    login,
    signup,
    logout,
    updateProfile,
    updateProfilePicture,
    forgotPassword,
    resetPassword,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
