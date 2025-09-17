import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  MapPin, 
  Phone, 
  Mail, 
  Facebook, 
  Youtube, 
  Linkedin,
  Send
} from "lucide-react";
import { Link } from "react-router-dom";

const Footer = () => {
  const quickLinks = [
    { name: "Sản phẩm", href: "/products" },
    { name: "Dịch vụ", href: "/services" },
    { name: "Tin tức", href: "/news" },
    { name: "Tuyển dụng", href: "/careers" },
    { name: "Liên hệ", href: "/contact" }
  ];

  const productLinks = [
    { name: "Giống GGP", href: "/products/ggp" },
    { name: "Giống GP", href: "/products/gp" },
    { name: "Giống PS", href: "/products/ps" },
    { name: "Catalog sản phẩm", href: "/catalog" },
    { name: "So sánh giống", href: "/compare" }
  ];

  const serviceLinks = [
    { name: "Tư vấn di truyền", href: "/services/genetic" },
    { name: "Hỗ trợ thú y", href: "/services/veterinary" },
    { name: "Đào tạo", href: "/services/training" },
    { name: "Đặt lịch tham quan", href: "/visit" },
    { name: "Yêu cầu báo giá", href: "/quote" }
  ];

  return (
    <footer className="bg-primary text-primary-foreground">
      {/* Newsletter Section */}
      <div className="border-b border-primary-foreground/20">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-4xl mx-auto text-center">
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Nhận tin tức mới nhất về chăn nuôi
            </h3>
            <p className="text-primary-foreground/80 mb-8">
              Cập nhật thông tin thị trường, kỹ thuật chăn nuôi và ưu đãi đặc biệt
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <Input 
                placeholder="Nhập email của bạn"
                className="bg-white/10 border-white/20 text-white placeholder:text-white/60"
              />
              <Button variant="cta" className="bg-white text-primary hover:bg-white/90">
                <Send className="h-4 w-4 mr-2" />
                Đăng ký
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-1">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
                <span className="text-primary font-bold text-xl">MF</span>
              </div>
              <div>
                <h3 className="text-xl font-bold">Metafarm</h3>
                <p className="text-primary-foreground/80 text-sm">Chăn nuôi heo chất lượng cao</p>
              </div>
            </div>
            <p className="text-primary-foreground/80 mb-6 text-sm leading-relaxed">
              Công ty trẻ chuyên chăn nuôi heo, nhập khẩu và phân phối heo giống GGP, GP, PS 
              từ các quốc gia có ngành chăn nuôi phát triển. Cam kết cung cấp những con giống 
              chất lượng cao nhất, đảm bảo an toàn cho khách hàng.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <MapPin className="h-4 w-4 text-accent flex-shrink-0 mt-0.5" />
                <div className="text-sm text-primary-foreground/80">
                  <div className="font-medium mb-1">Văn phòng:</div>
                  <div>4 ngách 10/461 Ng. 461 Đ. Nguyễn Văn Linh</div>
                  <div>Sài Đồng, Long Biên, Hà Nội</div>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <MapPin className="h-4 w-4 text-accent flex-shrink-0 mt-0.5" />
                <div className="text-sm text-primary-foreground/80">
                  <div className="font-medium mb-1">Trại hạt nhân:</div>
                  <div>Hợp tác xã Metafarm, xã Việt Hoà</div>
                  <div>huyện Khoái Châu, tỉnh Hưng Yên</div>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-4 w-4 text-accent flex-shrink-0" />
                <div className="text-sm text-primary-foreground/80">
                  <div>0975 885 946 | 0868 222 136</div>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="h-4 w-4 text-accent flex-shrink-0" />
                <span className="text-sm text-primary-foreground/80">
                  info@metafarm.vn
                </span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Liên kết nhanh</h4>
            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-primary-foreground/80 hover:text-accent transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Products */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Sản phẩm</h4>
            <ul className="space-y-3">
              {productLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-primary-foreground/80 hover:text-accent transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Dịch vụ</h4>
            <ul className="space-y-3">
              {serviceLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-primary-foreground/80 hover:text-accent transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-primary-foreground/20">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-primary-foreground/80">
              © 2024 Metafarm. Tất cả quyền được bảo lưu.
            </div>
            
            {/* Social Links */}
            <div className="flex items-center space-x-4">
              <span className="text-sm text-primary-foreground/80">Theo dõi chúng tôi:</span>
              <div className="flex space-x-3">
                <a href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  <Facebook className="h-5 w-5" />
                </a>
                <a href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  <Youtube className="h-5 w-5" />
                </a>
                <a href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  <Linkedin className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;