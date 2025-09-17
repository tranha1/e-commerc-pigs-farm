from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .sql_models import Medicine, Pig, CmsContentEntry, CmsNewsEntry, NewsCategory
import json

@require_http_methods(["GET"])
def api_health(request):
    """Health check endpoint"""
    return JsonResponse({
        "status": "ok", 
        "service": "pig_farm_api",
        "version": "1.0.0"
    })

@require_http_methods(["GET"])
def api_medicines(request):
    """API endpoint for medicines"""
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        search = request.GET.get('search', '')
        published_only = request.GET.get('published', 'true').lower() == 'true'
        
        # Build queryset
        queryset = Medicine.objects.all()
        
        if published_only:
            queryset = queryset.filter(is_published=True, is_deleted=False)
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Order by updated_at desc
        queryset = queryset.order_by('-updated_at')
        
        # Paginate
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Serialize data
        medicines = []
        for medicine in page_obj:
            medicines.append({
                'id': medicine.id,
                'name': medicine.name,
                'packaging': medicine.packaging,
                'price_unit': float(medicine.price_unit) if medicine.price_unit else None,
                'price_total': float(medicine.price_total) if medicine.price_total else None,
                'is_published': medicine.is_published,
                'published_at': medicine.published_at.isoformat() if medicine.published_at else None,
                'updated_at': medicine.updated_at.isoformat() if medicine.updated_at else None,
            })
        
        return JsonResponse({
            'status': 'success',
            'data': medicines,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(["GET"])
def api_pigs(request):
    """API endpoint for pigs"""
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        search = request.GET.get('search', '')
        published_only = request.GET.get('published', 'true').lower() == 'true'
        
        queryset = Pig.objects.all()
        
        if published_only:
            queryset = queryset.filter(is_published=True, is_deleted=False)
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        queryset = queryset.order_by('-updated_at')
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        pigs = []
        for pig in page_obj:
            pigs.append({
                'id': pig.id,
                'name': pig.name,
                'price': float(pig.price) if pig.price else None,
                'is_published': pig.is_published,
                'published_at': pig.published_at.isoformat() if pig.published_at else None,
                'updated_at': pig.updated_at.isoformat() if pig.updated_at else None,
            })
        
        return JsonResponse({
            'status': 'success',
            'data': pigs,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_news_articles(request):
    """API endpoint for news articles"""
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        search = request.GET.get('search', '')
        category = request.GET.get('category', '')
        featured_only = request.GET.get('featured', 'false').lower() == 'true'
        published_only = request.GET.get('published', 'true').lower() == 'true'
        
        # Build queryset - get news entries only (kind_id=2)
        queryset = CmsNewsEntry.get_news_queryset()
        
        if published_only:
            queryset = queryset.filter(is_published=True, is_deleted=False)
        
        # Note: featured_only not implemented in cms_content_entry yet
        # Could be added as a boolean field later
        
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        # Note: category filtering not implemented yet
        # Could be added as a field or relationship later
        
        # Order by published_at desc, then by created_at desc
        queryset = queryset.order_by('-published_at', '-created_at')
        
        # Paginate
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Serialize data
        articles = []
        for entry in page_obj:
            articles.append({
                'id': entry.id,
                'title': entry.title,
                'slug': entry.slug,
                'summary': entry.summary,
                'content': entry.get_content_text(),
                'featured_image': entry.get_featured_image_url(),
                'category_id': None,  # Not implemented in cms_content_entry yet
                'author': entry.author_name,
                'read_time': entry.get_read_time(),
                'view_count': 0,  # Not tracked in cms_content_entry yet
                'tags': entry.get_tags_list(),
                'meta_title': entry.seo_title,
                'meta_description': entry.seo_desc,
                'is_featured': False,  # Not implemented yet
                'is_published': entry.is_published,
                'published_at': entry.published_at.isoformat() if entry.published_at else None,
                'created_at': entry.created_at.isoformat() if entry.created_at else None,
                'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
            })
        
        return JsonResponse({
            'status': 'success',
            'data': articles,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_news_article_detail(request, article_id):
    """API endpoint for single news article detail from cms_content_entry"""
    try:
        entry = CmsNewsEntry.objects.get(
            id=article_id, 
            kind_id=2,  # news kind
            is_published=True, 
            is_deleted=False
        )
        
        # Note: View count not tracked in cms_content_entry yet
        # Could be added as a field later
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': entry.id,
                'title': entry.title,
                'slug': entry.slug,
                'summary': entry.summary,
                'content': entry.get_content_text(),
                'featured_image': entry.get_featured_image_url(),
                'category_id': None,  # Not implemented yet
                'author': entry.author_name,
                'read_time': entry.get_read_time(),
                'view_count': 0,  # Not tracked yet
                'tags': entry.get_tags_list(),
                'meta_title': entry.seo_title,
                'meta_description': entry.seo_desc,
                'is_featured': False,  # Not implemented yet
                'is_published': entry.is_published,
                'published_at': entry.published_at.isoformat() if entry.published_at else None,
                'created_at': entry.created_at.isoformat() if entry.created_at else None,
                'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
            }
        })
        
    except CmsNewsEntry.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Article not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_news_categories(request):
    """API endpoint for news categories"""
    try:
        # Get query parameters
        published_only = request.GET.get('published', 'true').lower() == 'true'
        
        # Build queryset
        queryset = NewsCategory.objects.all()
        
        if published_only:
            queryset = queryset.filter(is_published=True, is_deleted=False)
        
        # Order by sort_order, then by name
        queryset = queryset.order_by('sort_order', 'name')
        
        # Serialize data
        categories = []
        for category in queryset:
            categories.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'description': category.description,
                'color': category.color,
                'icon': category.icon,
                'parent_id': category.parent_id,
                'sort_order': category.sort_order,
                'is_published': category.is_published,
                'published_at': category.published_at.isoformat() if category.published_at else None,
                'created_at': category.created_at.isoformat() if category.created_at else None,
                'updated_at': category.updated_at.isoformat() if category.updated_at else None,
            })
        
        return JsonResponse({
            'status': 'success',
            'data': categories
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_pig_detail(request, pig_id):
    """API endpoint for single pig detail"""
    try:
        pig = Pig.objects.get(
            id=pig_id, 
            is_published=True, 
            is_deleted=False
        )
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': pig.id,
                'name': pig.name,
                'price': float(pig.price) if pig.price else None,
                'is_published': pig.is_published,
                'published_at': pig.published_at.isoformat() if pig.published_at else None,
                'updated_at': pig.updated_at.isoformat() if pig.updated_at else None,
            }
        })
        
    except Pig.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Pig not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_medicine_detail(request, medicine_id):
    """API endpoint for single medicine detail"""
    try:
        medicine = Medicine.objects.get(
            id=medicine_id, 
            is_published=True, 
            is_deleted=False
        )
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': medicine.id,
                'name': medicine.name,
                'packaging': medicine.packaging,
                'price_unit': float(medicine.price_unit) if medicine.price_unit else None,
                'price_total': float(medicine.price_total) if medicine.price_total else None,
                'is_published': medicine.is_published,
                'published_at': medicine.published_at.isoformat() if medicine.published_at else None,
                'updated_at': medicine.updated_at.isoformat() if medicine.updated_at else None,
            }
        })
        
    except Medicine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Medicine not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)