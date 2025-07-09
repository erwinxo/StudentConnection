import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Paper,
  Avatar,
  Fab,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Add,
  Search,
  FilterList,
  Download,
  Comment,
  ExpandMore,
  OpenInNew
} from '@mui/icons-material';
import { useForm } from 'react-hook-form';
import { postsAPI, commentsAPI } from '../api/api';

const PostsTab = () => {
  const [posts, setPosts] = useState([]);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');
  const [selectedPost, setSelectedPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  
  const createForm = useForm();

  const fetchPosts = useCallback(async () => {
    try {
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (filterType) params.post_type = filterType;
      
      const response = await postsAPI.getPosts(params);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  }, [searchTerm, filterType]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const onCreatePost = async (data) => {
    try {
      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('content', data.content);
      formData.append('post_type', data.post_type);
      formData.append('tags', data.tags || '');
      
      if (data.post_type === 'jobs') {
        formData.append('job_link', data.job_link);
        formData.append('company', data.company || '');
        formData.append('location', data.location || '');
      }
      
      if (data.post_type === 'notes' && data.document?.[0]) {
        formData.append('document', data.document[0]);
      }

      await postsAPI.createPost(formData);
      setCreateDialogOpen(false);
      createForm.reset();
      fetchPosts();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const fetchComments = async (postId) => {
    try {
      const response = await commentsAPI.getPostComments(postId);
      setComments(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const handlePostClick = async (post) => {
    setSelectedPost(post);
    await fetchComments(post.id);
  };

  const addComment = async () => {
    if (!newComment.trim()) return;
    
    try {
      await commentsAPI.createComment({
        content: newComment,
        post_id: selectedPost.id
      });
      setNewComment('');
      await fetchComments(selectedPost.id);
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  const PostCard = ({ post }) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar src={post.author_profile_picture} sx={{ mr: 2 }}>
            {post.author_name[0]}
          </Avatar>
          <Box>
            <Typography variant="subtitle2">{post.author_name}</Typography>
            <Typography variant="caption" color="text.secondary">
              @{post.author_username}
            </Typography>
          </Box>
          <Chip 
            label={post.post_type} 
            color="primary" 
            size="small" 
            sx={{ ml: 'auto' }}
          />
        </Box>
        
        <Typography variant="h6" gutterBottom>
          {post.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {post.content}
        </Typography>
        
        {post.tags.length > 0 && (
          <Box sx={{ mb: 2 }}>
            {post.tags.map((tag, index) => (
              <Chip key={index} label={tag} size="small" sx={{ mr: 1, mb: 1 }} />
            ))}
          </Box>
        )}
        
        {post.document_url && (
          <Button
            startIcon={<Download />}
            onClick={() => window.open(post.document_url, '_blank')}
            sx={{ mb: 1 }}
          >
            Download {post.document_name}
          </Button>
        )}
        
        {post.job_link && (
          <Box>
            <Button
              startIcon={<OpenInNew />}
              onClick={() => window.open(post.job_link, '_blank')}
              variant="outlined"
            >
              View Job
            </Button>
            {post.company && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Company: {post.company}
              </Typography>
            )}
            {post.location && (
              <Typography variant="body2">
                Location: {post.location}
              </Typography>
            )}
          </Box>
        )}
      </CardContent>
      
      <CardActions>
        <Button
          startIcon={<Comment />}
          onClick={() => handlePostClick(post)}
        >
          Comments ({post.comments_count})
        </Button>
      </CardActions>
    </Card>
  );

  return (
    <Box sx={{ mt: 2 }}>
      {/* Search and Filter */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search posts, tags, or users..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <Search sx={{ mr: 1 }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Filter by type</InputLabel>
              <Select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                startAdornment={<FilterList sx={{ mr: 1 }} />}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="notes">Notes</MenuItem>
                <MenuItem value="jobs">Jobs</MenuItem>
                <MenuItem value="threads">Threads</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Posts */}
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {/* Create Post FAB */}
      <Fab
        color="primary"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setCreateDialogOpen(true)}
      >
        <Add />
      </Fab>

      {/* Create Post Dialog */}
      <Dialog 
        open={createDialogOpen} 
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Create New Post</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <TextField
              fullWidth
              label="Title"
              margin="normal"
              {...createForm.register('title', { required: true })}
            />
            <TextField
              fullWidth
              label="Content"
              margin="normal"
              multiline
              rows={4}
              {...createForm.register('content', { required: true })}
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Post Type</InputLabel>
              <Select {...createForm.register('post_type', { required: true })}>
                <MenuItem value="notes">Notes</MenuItem>
                <MenuItem value="jobs">Jobs</MenuItem>
                <MenuItem value="threads">Threads</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Tags (comma separated)"
              margin="normal"
              {...createForm.register('tags')}
            />
            
            {createForm.watch('post_type') === 'notes' && (
              <TextField
                fullWidth
                type="file"
                label="Document"
                margin="normal"
                InputLabelProps={{ shrink: true }}
                {...createForm.register('document')}
              />
            )}
            
            {createForm.watch('post_type') === 'jobs' && (
              <>
                <TextField
                  fullWidth
                  label="Job Link"
                  margin="normal"
                  {...createForm.register('job_link')}
                />
                <TextField
                  fullWidth
                  label="Company"
                  margin="normal"
                  {...createForm.register('company')}
                />
                <TextField
                  fullWidth
                  label="Location"
                  margin="normal"
                  {...createForm.register('location')}
                />
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button onClick={createForm.handleSubmit(onCreatePost)} variant="contained">
            Create Post
          </Button>
        </DialogActions>
      </Dialog>

      {/* Comments Dialog */}
      <Dialog
        open={!!selectedPost}
        onClose={() => setSelectedPost(null)}
        maxWidth="md"
        fullWidth
      >
        {selectedPost && (
          <>
            <DialogTitle>{selectedPost.title}</DialogTitle>
            <DialogContent>
              <Typography paragraph>{selectedPost.content}</Typography>
              
              <Typography variant="h6" gutterBottom>
                Comments
              </Typography>
              
              {comments.map((comment) => (
                <Card key={comment.id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Avatar src={comment.author_profile_picture} sx={{ width: 24, height: 24, mr: 1 }}>
                        {comment.author_name[0]}
                      </Avatar>
                      <Typography variant="subtitle2">
                        {comment.author_name}
                      </Typography>
                    </Box>
                    <Typography variant="body2">
                      {comment.content}
                    </Typography>
                    
                    {comment.replies.length > 0 && (
                      <Accordion sx={{ mt: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <Typography variant="caption">
                            {comment.replies.length} replies
                          </Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                          {comment.replies.map((reply) => (
                            <Box key={reply.id} sx={{ ml: 2, mb: 1 }}>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Avatar src={reply.author_profile_picture} sx={{ width: 20, height: 20, mr: 1 }}>
                                  {reply.author_name[0]}
                                </Avatar>
                                <Typography variant="caption">
                                  {reply.author_name}
                                </Typography>
                              </Box>
                              <Typography variant="body2">
                                {reply.content}
                              </Typography>
                            </Box>
                          ))}
                        </AccordionDetails>
                      </Accordion>
                    )}
                  </CardContent>
                </Card>
              ))}
              
              <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                <TextField
                  fullWidth
                  placeholder="Add a comment..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <Button onClick={addComment} variant="contained">
                  Post
                </Button>
              </Box>
            </DialogContent>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default PostsTab;
