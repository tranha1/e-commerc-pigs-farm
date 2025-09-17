import { useParams, Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  ArrowLeft, 
  Calendar, 
  Clock, 
  DollarSign,
  Package,
  Share2,
  Facebook,
  Twitter,
  Link as LinkIcon,
  ShoppingCart,
  Heart,
  Star,
  Info,
  Award,
  Truck
} from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useProductDetail } from "@/hooks/useProductDetail";
import { usePigs, useMedicines } from "@/hooks/useApi";
import { formatCurrency } from "@/lib/utils";

const ProductDetail = () => {
  const { type, id } = useParams<{ type: 'pig' | 'medicine'; id: string }>();
  const navigate = useNavigate();
  const productId = id ? parseInt(id) : undefined;
  const { product, loading, error } = useProductDetail(type!, productId);
  
  // Get related products
  const { data: pigsData } = usePigs({ published: true });
  const { data: medicinesData } = useMedicines({ published: true });

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleShare = (platform: string) => {
    if (!product) return;
    
    const url = window.location.href;
    const title = product.name;
    
    switch (platform) {
      case 'facebook':
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
        break;
      case 'twitter':
        window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
        break;
      case 'copy':
        navigator.clipboard.writeText(url);
        alert('Đã sao chép link!');
        break;
    }
  };

  const getRelatedProducts = () => {
    if (type === 'pig' && pigsData?.data) {
      return pigsData.data.filter(p => p.id !== productId).slice(0, 3);
    } else if (type === 'medicine' && medicinesData?.data) {
      return medicinesData.data.filter(m => m.id !== productId).slice(0, 3);
    }
    return [];
  };

  const getProductTypeLabel = () => {
    return type === 'pig' ? 'Heo giống' : 'Thuốc thú y';
  };

  const getProductFeatures = () => {
    if (type === 'pig') {
      return [
        { icon: <Award className="h-5 w-5" />, label: "Giống nhập khẩu", value: "Chất lượng cao" },
        { icon: <Star className="h-5 w-5" />, label: "Phả hệ rõ ràng", value: "Đầy đủ giấy tờ" },
        { icon: <Heart className="h-5 w-5" />, label: "Sức khỏe", value: "Kiểm tra định kỳ" },
        { icon: <Truck className="h-5 w-5" />, label: "Vận chuyển", value: "An toàn, nhanh chóng" }
      ];
    } else {
      return [
        { icon: <Package className="h-5 w-5" />, label: "Đóng gói", value: (product as any)?.packaging || "Tiêu chuẩn" },
        { icon: <Award className="h-5 w-5" />, label: "Chất lượng", value: "Đạt tiêu chuẩn GMP" },
        { icon: <Clock className="h-5 w-5" />, label: "Hạn sử dụng", value: "Theo quy định" },
        { icon: <Truck className="h-5 w-5" />, label: "Giao hàng", value: "Toàn quốc" }
      ];
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <Skeleton className="h-8 w-32 mb-6" />
            <Skeleton className="h-12 w-3/4 mb-4" />
            <Skeleton className="h-6 w-1/2 mb-8" />
            <div className="grid md:grid-cols-3 gap-8">
              <div className="md:col-span-2">
                <Skeleton className="h-64 w-full mb-6" />
                <Skeleton className="h-32 w-full" />
              </div>
              <div>
                <Skeleton className="h-48 w-full" />
              </div>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-2xl font-bold text-foreground mb-4">
              Không tìm thấy sản phẩm
            </h1>
            <p className="text-muted-foreground mb-8">
              Sản phẩm bạn đang tìm kiếm không tồn tại hoặc đã bị xóa.
            </p>
            <Button onClick={() => navigate('/products')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Quay lại danh sách sản phẩm
            </Button>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Back Button */}
          <Button 
            variant="ghost" 
            onClick={() => navigate('/products')}
            className="mb-6"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Quay lại danh sách sản phẩm
          </Button>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              {/* Product Header */}
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-4">
                  <Badge variant="secondary">{getProductTypeLabel()}</Badge>
                  {product.is_published && (
                    <Badge variant="default" className="bg-green-500">
                      Đang bán
                    </Badge>
                  )}
                </div>
                
                <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                  {product.name}
                </h1>
                
                <div className="flex items-center gap-6 text-sm text-muted-foreground">
                  <span className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Cập nhật: {formatDate(product.updated_at)}
                  </span>
                  <span className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    ID: #{product.id}
                  </span>
                </div>
              </div>

              {/* Product Image Placeholder */}
              <div className="mb-8">
                <div className="bg-muted rounded-lg h-96 flex items-center justify-center">
                  <div className="text-center">
                    <Package className="h-24 w-24 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Hình ảnh sản phẩm</p>
                    <p className="text-sm text-muted-foreground">{product.name}</p>
                  </div>
                </div>
              </div>

              {/* Product Features */}
              <Card className="mb-8">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Info className="h-5 w-5" />
                    Thông tin sản phẩm
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    {getProductFeatures().map((feature, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg">
                        <div className="text-primary">
                          {feature.icon}
                        </div>
                        <div>
                          <div className="font-medium text-foreground">{feature.label}</div>
                          <div className="text-sm text-muted-foreground">{feature.value}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Product Description */}
              <Card>
                <CardHeader>
                  <CardTitle>Mô tả chi tiết</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-gray max-w-none">
                    {type === 'pig' ? (
                      <div>
                        <h3>Giống {product.name}</h3>
                        <p>
                          {product.name} là một trong những dòng giống heo chất lượng cao được nhập khẩu từ các nước 
                          có nền chăn nuôi phát triển. Giống này được chọn lọc kỹ càng với phả hệ rõ ràng, 
                          đảm bảo tính ổn định về di truyền và khả năng sản xuất cao.
                        </p>
                        <h4>Đặc điểm nổi bật:</h4>
                        <ul>
                          <li>Tốc độ tăng trọng nhanh</li>
                          <li>Tỷ lệ thịt nạc cao</li>
                          <li>Khả năng chống chịu bệnh tật tốt</li>
                          <li>Thích nghi với khí hậu Việt Nam</li>
                          <li>Được kiểm tra sức khỏe định kỳ</li>
                        </ul>
                      </div>
                    ) : (
                      <div>
                        <h3>{product.name}</h3>
                        <p>
                          {product.name} là sản phẩm thuốc thú y chất lượng cao, được sản xuất theo tiêu chuẩn GMP, 
                          đảm bảo an toàn và hiệu quả trong việc chăm sóc sức khỏe đàn heo.
                        </p>
                        <h4>Thông tin sản phẩm:</h4>
                        <ul>
                          <li>Đóng gói: {(product as any).packaging || 'Theo tiêu chuẩn'}</li>
                          <li>Bảo quản: Nơi khô ráo, thoáng mát</li>
                          <li>Xuất xứ: Việt Nam</li>
                          <li>Chất lượng: Đạt tiêu chuẩn quốc gia</li>
                        </ul>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Price & Actions */}
              <Card>
                <CardContent className="p-6">
                  <div className="text-center mb-6">
                    {(product as any).price ? (
                      <div>
                        <div className="text-3xl font-bold text-primary mb-2">
                          {formatCurrency((product as any).price)}
                        </div>
                        {type === 'medicine' && (product as any).price_unit && (
                          <div className="text-sm text-muted-foreground">
                            Đơn giá: {formatCurrency((product as any).price_unit)}
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-lg font-semibold text-foreground mb-2">
                        Liên hệ để biết giá
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <Button className="w-full" size="lg">
                      <ShoppingCart className="h-4 w-4 mr-2" />
                      Đặt hàng ngay
                    </Button>
                    <Button variant="outline" className="w-full">
                      <Heart className="h-4 w-4 mr-2" />
                      Yêu thích
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Share */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Chia sẻ sản phẩm</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleShare('facebook')}
                      className="flex-1"
                    >
                      <Facebook className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleShare('twitter')}
                      className="flex-1"
                    >
                      <Twitter className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleShare('copy')}
                      className="flex-1"
                    >
                      <LinkIcon className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Contact */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Cần hỗ trợ?</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm">
                    <div>
                      <div className="font-medium">Hotline</div>
                      <div className="text-muted-foreground">0975 885 946</div>
                    </div>
                    <div>
                      <div className="font-medium">Email</div>
                      <div className="text-muted-foreground">info@metafarm.vn</div>
                    </div>
                    <Button variant="outline" className="w-full mt-3" asChild>
                      <Link to="/contact">Liên hệ tư vấn</Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Related Products */}
          {getRelatedProducts().length > 0 && (
            <section className="mt-16">
              <h2 className="text-2xl font-bold text-foreground mb-8">
                Sản phẩm liên quan
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                {getRelatedProducts().map((relatedProduct) => (
                  <Card key={relatedProduct.id} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-6">
                      <div className="text-center mb-4">
                        <Package className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
                        <h3 className="font-semibold text-foreground mb-2">
                          {relatedProduct.name}
                        </h3>
                        {(relatedProduct as any).price && (
                          <div className="text-lg font-bold text-primary">
                            {formatCurrency((relatedProduct as any).price)}
                          </div>
                        )}
                      </div>
                      <Button 
                        variant="outline" 
                        className="w-full"
                        asChild
                      >
                        <Link to={`/products/${type}/${relatedProduct.id}`}>
                          Xem chi tiết
                        </Link>
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ProductDetail;