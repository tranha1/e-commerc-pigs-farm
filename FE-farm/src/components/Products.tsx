import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Star, 
  Shield, 
  Award,
  ArrowRight,
  Zap
} from "lucide-react";
import { useTranslation } from "react-i18next";

const Products = () => {
  const { t } = useTranslation();
  
  const productCategories = [
    {
      id: "ggp",
      title: t("products.ggp"),
      description: "Dòng ông bà, chất lượng gen cao nhất, nhập khẩu trực tiếp",
      image: "🐓",
      features: ["Tỷ lệ sống cao 98%", "Khả năng sinh sản tối ưu", "Kháng bệnh tự nhiên"],
      badge: "Premium",
      badgeColor: "bg-accent text-accent-foreground"
    },
    {
      id: "gp", 
      title: t("products.gp"),
      description: "Dòng cha mẹ, chất lượng ổn định, phù hợp quy mô trung bình",
      image: "🐔",
      features: ["Tăng trọng nhanh", "Tiêu thụ thức ăn hiệu quả", "Dễ chăm sóc"],
      badge: "Phổ biến",
      badgeColor: "bg-primary text-primary-foreground"
    },
    {
      id: "ps",
      title: t("products.ps"),
      description: "Dòng thương phẩm, giá cả phù hợp, chất lượng đảm bảo",
      image: "🐣",
      features: ["Giá cả hợp lý", "Phù hợp trang trại nhỏ", "Hỗ trợ kỹ thuật"],
      badge: "Tiết kiệm",
      badgeColor: "bg-secondary text-secondary-foreground"
    }
  ];

  const highlights = [
    {
      icon: Shield,
      title: "Kiểm dịch nghiêm ngặt",
      description: "100% đàn giống được kiểm dịch theo tiêu chuẩn quốc tế"
    },
    {
      icon: Award,
      title: "Chứng nhận chất lượng",
      description: "Được cấp phép nhập khẩu và phân phối chính thức"
    },
    {
      icon: Zap,
      title: "Giao hàng nhanh chóng",
      description: "Hệ thống logistics chuyên nghiệp, giao hàng trong 24h"
    }
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="inline-block px-4 py-2 bg-accent/10 text-accent rounded-full text-sm font-medium mb-4">
            Sản phẩm chính
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
            {t("products.title")}
          </h2>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Cung cấp đầy đủ các dòng giống từ GGP đến PS, đáp ứng mọi nhu cầu 
            chăn nuôi từ quy mô nhỏ đến trang trại lớn
          </p>
        </div>

        {/* Product Categories */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {productCategories.map((category) => (
            <Card key={category.id} className="group hover:shadow-strong transition-all duration-300 hover:-translate-y-2 border-border/50 relative overflow-hidden">
              <div className="absolute top-4 right-4">
                <Badge className={category.badgeColor}>
                  {category.badge}
                </Badge>
              </div>
              
              <CardHeader className="text-center pb-4">
                <div className="text-6xl mb-4">{category.image}</div>
                <CardTitle className="text-xl mb-2">{category.title}</CardTitle>
                <CardDescription className="text-muted-foreground">
                  {category.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3 mb-6">
                  {category.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center text-sm">
                      <Star className="h-4 w-4 text-accent mr-2 flex-shrink-0" />
                      <span className="text-muted-foreground">{feature}</span>
                    </div>
                  ))}
                </div>
                
                <div className="space-y-3">
                  <Button className="w-full group">
                    Xem chi tiết
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                  <Button variant="outline" className="w-full">
                    Yêu cầu báo giá
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Highlights */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {highlights.map((highlight, index) => {
            const IconComponent = highlight.icon;
            return (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <IconComponent className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  {highlight.title}
                </h3>
                <p className="text-muted-foreground text-sm">
                  {highlight.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* CTA Section */}
        <div className="text-center bg-muted/50 rounded-2xl p-8 md:p-12">
          <h3 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
            Cần tư vấn chọn giống phù hợp?
          </h3>
          <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
            Đội ngũ chuyên gia của chúng tôi sẽ tư vấn miễn phí để bạn chọn được 
            dòng giống phù hợp nhất với mục tiêu và điều kiện chăn nuôi
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="hero" size="lg">
              Tư vấn miễn phí ngay
            </Button>
            <Button variant="outline" size="lg">
              Tải catalog sản phẩm
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Products;