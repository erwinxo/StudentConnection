import React, { useState, useCallback } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Avatar,
  Paper,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Card,
  CardContent,
  Input,
  CircularProgress
} from '@mui/material';
import { Edit, PhotoCamera } from '@mui/icons-material';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { postsAPI } from '../api/api';

const ProfileTab = () => {
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [userPosts, setUserPosts] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadingPicture, setUploadingPicture] = useState(false);
  const { user, updateProfile, updateProfilePicture } = useAuth();
  const editForm = useForm({
    defaultValues: {
      name: user?.name || '',
      username: user?.username || '',
      bio: user?.bio || ''
    }
  });

  const fetchUserPosts = useCallback(async () => {
    try {
      const response = await postsAPI.getUserPosts(user.username);
      setUserPosts(response.data);
    } catch (error) {
      console.error('Error fetching user posts:', error);
    }
  }, [user?.username]);

  React.useEffect(() => {
    if (user?.username) {
      fetchUserPosts();
    }
  }, [user, fetchUserPosts]);

  const onUpdateProfile = async (data) => {
    try {
      await updateProfile(data);
      setEditDialogOpen(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('File size must be less than 5MB');
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleProfilePictureUpload = async () => {
    if (!selectedFile) return;
    
    setUploadingPicture(true);
    try {
      await updateProfilePicture(selectedFile);
      setSelectedFile(null);
      // Reset the file input
      const fileInput = document.getElementById('profile-picture-input');
      if (fileInput) fileInput.value = '';
    } catch (error) {
      console.error('Error uploading profile picture:', error);
      alert('Failed to upload profile picture');
    } finally {
      setUploadingPicture(false);
    }
  };

  const handleEditClick = () => {
    editForm.reset({
      name: user?.name || '',
      username: user?.username || '',
      bio: user?.bio || ''
    });
    setSelectedFile(null);
    setEditDialogOpen(true);
  };

  return (
    <Box sx={{ mt: 2 }}>
      {/* Profile Information */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item>
            <Avatar 
              src={user?.profile_picture} 
              sx={{ width: 100, height: 100 }}
            >
              {user?.name?.[0]}
            </Avatar>
          </Grid>
          <Grid item xs>
            <Typography variant="h4" gutterBottom>
              {user?.name}
            </Typography>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              @{user?.username}
            </Typography>
            <Typography variant="body1" paragraph>
              {user?.bio || 'No bio available'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Email: {user?.email}
            </Typography>
          </Grid>
          <Grid item>
            <Button
              variant="outlined"
              startIcon={<Edit />}
              onClick={handleEditClick}
            >
              Edit Profile
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* User Posts */}
      <Typography variant="h5" gutterBottom>
        My Posts ({userPosts.length})
      </Typography>
      
      {userPosts.map((post) => (
        <Card key={post.id} sx={{ mb: 2 }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
              <Typography variant="h6">
                {post.title}
              </Typography>
              <Typography variant="caption" color="primary">
                {post.post_type.toUpperCase()}
              </Typography>
            </Box>
            
            <Typography variant="body2" color="text.secondary" paragraph>
              {post.content}
            </Typography>
            
            {post.tags.length > 0 && (
              <Box sx={{ mb: 2 }}>
                {post.tags.map((tag, index) => (
                  <Typography 
                    key={index} 
                    variant="caption" 
                    sx={{ 
                      mr: 1, 
                      px: 1, 
                      py: 0.5, 
                      bgcolor: 'grey.200', 
                      borderRadius: 1 
                    }}
                  >
                    #{tag}
                  </Typography>
                ))}
              </Box>
            )}
            
            <Typography variant="caption" color="text.secondary">
              {post.comments_count} comments • {new Date(post.created_at).toLocaleDateString()}
            </Typography>
            
            {post.document_url && (
              <Box sx={{ mt: 1 }}>
                <Button 
                  size="small" 
                  onClick={() => window.open(post.document_url, '_blank')}
                >
                  Download {post.document_name}
                </Button>
              </Box>
            )}
            
            {post.job_link && (
              <Box sx={{ mt: 1 }}>
                <Button 
                  size="small" 
                  onClick={() => window.open(post.job_link, '_blank')}
                >
                  View Job Opening
                </Button>
                {post.company && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    Company: {post.company}
                  </Typography>
                )}
              </Box>
            )}
          </CardContent>
        </Card>
      ))}

      {/* Edit Profile Dialog */}
      <Dialog 
        open={editDialogOpen} 
        onClose={() => setEditDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Edit Profile</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            {/* Profile Picture Upload */}
            <Box sx={{ mb: 3, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                Profile Picture
              </Typography>
              <Avatar 
                src={user?.profile_picture} 
                sx={{ width: 80, height: 80, mx: 'auto', mb: 2 }}
              >
                {user?.name?.[0]}
              </Avatar>
              
              <Input
                id="profile-picture-input"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                sx={{ display: 'none' }}
              />
              <label htmlFor="profile-picture-input">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<PhotoCamera />}
                  sx={{ mr: 1 }}
                >
                  Choose Image
                </Button>
              </label>
              
              {selectedFile && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Selected: {selectedFile.name}
                  </Typography>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={handleProfilePictureUpload}
                    disabled={uploadingPicture}
                    sx={{ mt: 1 }}
                  >
                    {uploadingPicture ? (
                      <>
                        <CircularProgress size={16} sx={{ mr: 1 }} />
                        Uploading...
                      </>
                    ) : (
                      'Upload'
                    )}
                  </Button>
                </Box>
              )}
            </Box>

            <TextField
              fullWidth
              label="Name"
              margin="normal"
              {...editForm.register('name', { required: 'Name is required' })}
              error={!!editForm.formState.errors.name}
              helperText={editForm.formState.errors.name?.message}
            />
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              {...editForm.register('username', { required: 'Username is required' })}
              error={!!editForm.formState.errors.username}
              helperText={editForm.formState.errors.username?.message}
            />
            <TextField
              fullWidth
              label="Bio"
              margin="normal"
              multiline
              rows={4}
              {...editForm.register('bio')}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={editForm.handleSubmit(onUpdateProfile)} 
            variant="contained"
          >
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProfileTab;
