# Ipswich Retail Shop - Django E-commerce PoC

A modern, responsive e-commerce proof of concept built with Django, demonstrating Model-View-Template (MVT) architecture and DevOps principles.

## 🎯 Project Overview

This PoC addresses the challenges of monolithic architecture by implementing:
- **MVT Architecture**: Clean separation of concerns with reusable components
- **DevOps Principles**: Automated testing, CI/CD pipeline, and containerization
- **Modern Frontend**: Responsive design with Bootstrap 5 and interactive features
- **Scalable Backend**: Django ORM with optimized database queries

## 🚀 Features

### Core Pages (4 + Admin)
1. **Home Page** - Hero section with featured products and categories
2. **Product List Page** - Browse products with search, filtering, and pagination
3. **Product Detail Page** - Individual product view with add to cart functionality
4. **Shopping Cart Page** - Cart management with quantity updates and removal
5. **Admin Page** - Django admin interface for product management

### Technical Features
- **Responsive Design** - Mobile-first approach with Bootstrap 5
- **Search & Filtering** - Real-time product search and category filtering
- **Shopping Cart** - Session-based cart with AJAX updates
- **Image Handling** - Product images with Pillow integration
- **User Authentication** - Django's built-in user system
- **Admin Interface** - Comprehensive admin panel for content management

## 🏗️ Project Structure

```
ecommerce_poc/
├── ecommerce_poc/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                    # Main application
│   ├── models.py           # Product, Category, Cart models
│   ├── views.py            # View functions and class-based views
│   ├── forms.py            # Django forms for cart functionality
│   ├── admin.py            # Admin interface configuration
│   ├── urls.py             # URL patterns
│   ├── context_processors.py # Global template context
│   ├── management/         # Custom management commands
│   ├── static/shop/        # Static files (CSS, JS, images)
│   └── templates/shop/     # HTML templates
├── manage.py
├── requirements.txt
├── setup.py                # Automated setup script
└── README.md
```

## 🛠️ Installation & Setup

### Quick Start (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd ecommerce_poc
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run automated setup:**
   ```bash
   python setup.py
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - **Main site**: http://127.0.0.1:8000
   - **Admin panel**: http://127.0.0.1:8000/admin
   - **Login**: admin / admin123

### Manual Setup

If you prefer manual setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Populate sample data:**
   ```bash
   python manage.py populate_data
   ```

5. **Start server:**
   ```bash
   python manage.py runserver
   ```

## 🎨 Design & UI

### Frontend Technologies
- **Bootstrap 5** - Responsive grid system and components
- **Font Awesome** - Icons and visual elements
- **Custom CSS** - Modern styling with CSS variables
- **JavaScript** - Interactive features and AJAX functionality

### Design Features
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Modern UI** - Clean, professional design with smooth animations
- **Interactive Elements** - Hover effects, loading states, and transitions
- **Accessibility** - ARIA labels and keyboard navigation support

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

### Test Coverage
- **Unit Tests** - Model methods and business logic
- **Integration Tests** - View functions and URL patterns
- **Form Tests** - Form validation and error handling

## 🚀 DevOps Features

### Development Environment
- **Docker Support** - Containerized development environment
- **Environment Variables** - Configuration management
- **Database Migrations** - Version-controlled schema changes

### CI/CD Pipeline (GitHub Actions)
- **Automated Testing** - Runs tests on every push
- **Code Quality** - Linting and formatting checks
- **Security Scanning** - Dependency vulnerability checks
- **Deployment** - Automated deployment to staging/production

### Monitoring & Logging
- **Application Logging** - Structured logging for debugging
- **Error Tracking** - Centralized error monitoring
- **Performance Metrics** - Database query optimization

## 📊 MVT Architecture Benefits

### Model Layer
- **Clean Data Structure** - Well-defined relationships and constraints
- **Business Logic** - Encapsulated in model methods
- **Database Abstraction** - Django ORM for database operations

### View Layer
- **Separation of Concerns** - Business logic separated from presentation
- **Reusable Views** - Class-based views for common patterns
- **API Endpoints** - AJAX endpoints for dynamic functionality

### Template Layer
- **Template Inheritance** - DRY principle with base templates
- **Reusable Components** - Modular template design
- **Context Processors** - Global template variables

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)
- **Testing**: In-memory SQLite

## 📈 Performance Optimizations

### Database
- **Query Optimization** - Select_related and prefetch_related
- **Database Indexing** - Optimized indexes for common queries
- **Connection Pooling** - Efficient database connections

### Frontend
- **Static File Optimization** - Minified CSS and JavaScript
- **Image Optimization** - Responsive images and lazy loading
- **Caching** - Template and database query caching

## 🛡️ Security Features

### Built-in Security
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Prevention** - Django ORM protection
- **XSS Protection** - Template auto-escaping
- **Secure Headers** - Security middleware configuration

### Authentication & Authorization
- **User Authentication** - Django's built-in auth system
- **Session Management** - Secure session handling
- **Admin Security** - Protected admin interface

## 📱 Mobile Responsiveness

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- **Touch-Friendly** - Large buttons and touch targets
- **Swipe Gestures** - Product image galleries
- **Mobile Navigation** - Collapsible navigation menu

## 🔄 API Endpoints

### AJAX Endpoints
- `POST /add-to-cart/` - Add product to cart
- `POST /cart/update/<id>/` - Update cart item quantity
- `POST /cart/remove/<id>/` - Remove item from cart

### Response Format
```json
{
    "success": true,
    "message": "Product added to cart successfully",
    "cart_items_count": 3
}
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up production database
- [ ] Configure static file serving
- [ ] Set up SSL certificate
- [ ] Configure email settings
- [ ] Set up monitoring and logging

### Docker Deployment
```bash
# Build image
docker build -t ipswich-retail .

# Run container
docker run -p 8000:8000 ipswich-retail
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Email**: support@ipswichretail.com
- **Documentation**: [Project Wiki](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)

## 🎉 Acknowledgments

- Django framework and community
- Bootstrap team for the CSS framework
- Font Awesome for the icon library
- All contributors and testers

---

**Built with ❤️ for Ipswich Retail Shop E-commerce PoC**