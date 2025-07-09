import React, { useState } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Tab,
  Tabs,
  IconButton,
  Avatar
} from '@mui/material';
import { Logout } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import PostsTab from '../components/PostsTab';
import ProfileTab from '../components/ProfileTab';

const MainPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            StudentConnect
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar src={user?.profile_picture} sx={{ width: 32, height: 32 }}>
              {user?.name?.[0]}
            </Avatar>
            <Typography variant="body2">
              {user?.name}
            </Typography>
            <IconButton color="inherit" onClick={handleLogout}>
              <Logout />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} centered>
            <Tab label="Posts" />
            <Tab label="Profile" />
          </Tabs>
        </Box>

        {tabValue === 0 && <PostsTab />}
        {tabValue === 1 && <ProfileTab />}
      </Container>
    </>
  );
};

export default MainPage;
