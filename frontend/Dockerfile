FROM nginx:alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Add custom config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend HTML
COPY index.html /usr/share/nginx/html/