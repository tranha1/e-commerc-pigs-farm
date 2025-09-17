import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Dna,
  Stethoscope,
  GraduationCap,
  ShieldCheck,
  ArrowRight,
  Users
} from "lucide-react";

const Services = () => {
  const services = [
    {
      icon: Dna,
      title: "Tư vấn di truyền",
      description: "Phân tích và tư vấn chọn giống phù hợp với mục tiêu chăn nuôi của bạn",
      features: ["Phân tích gen", "Chọn lọc giống", "Kế hoạch phối giống"],
      color: "text-primary"
    },
    {
      icon: Stethoscope,
      title: "Hỗ trợ thú y",
      description: "Đội ngũ bác sĩ thú y chuyên nghiệp hỗ trợ 24/7",
      features: ["Khám chữa bệnh", "Phòng bệnh", "Tư vấn dinh dưỡng"],
      color: "text-accent"
    },
    {
      icon: GraduationCap,
      title: "Đào tạo vận hành",
      description: "Chương trình đào tạo chăn nuôi chuyên nghiệp từ cơ bản đến nâng cao",
      features: ["Kỹ thuật chăn nuôi", "Quản lý trang trại", "An toàn sinh học"],
      color: "text-primary"
    },
    {
      icon: ShieldCheck,
      title: "Kiểm dịch & Chứng nhận",
      description: "Quy trình kiểm dịch nghiêm ngặt theo tiêu chuẩn quốc tế",
      features: ["Xét nghiệm bệnh", "Chứng nhận sức khỏe", "Theo dõi sau bán"],
      color: "text-accent"
    }
  ];

  return (
    <section className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="inline-block px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium mb-4">
            Dịch vụ chuyên nghiệp
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
            Giải pháp toàn diện cho chăn nuôi
          </h2>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Từ tư vấn chọn giống đến hỗ trợ kỹ thuật, chúng tôi đồng hành cùng bạn
            trong toàn bộ quá trình chăn nuôi
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {services.map((service, index) => {
            const IconComponent = service.icon;
            return (
              <Card key={index} className="group hover:shadow-strong transition-all duration-300 hover:-translate-y-2 border-border/50">
                <CardHeader className="text-center pb-4">
                  <div className={`w-16 h-16 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <IconComponent className={`h-8 w-8 ${service.color}`} />
                  </div>
                  <CardTitle className="text-xl mb-2">{service.title}</CardTitle>
                  <CardDescription className="text-muted-foreground">
                    {service.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 mb-6">
                    {service.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center text-sm text-muted-foreground">
                        <div className="w-1.5 h-1.5 bg-primary rounded-full mr-3" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <Button variant="outline" className="w-full group">
                    Tìm hiểu thêm
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Service Packages CTA */}
        <div className="bg-primary rounded-2xl p-8 md:p-12 text-center">
          <div className="max-w-3xl mx-auto">
            <Users className="h-16 w-16 text-primary-foreground mx-auto mb-6" />
            <h3 className="text-2xl md:text-3xl font-bold text-primary-foreground mb-4">
              Gói dịch vụ toàn diện
            </h3>
            <p className="text-primary-foreground/90 text-lg mb-8">
              Kết hợp tất cả dịch vụ trong một gói với mức giá ưu đãi.
              Được hàng trăm trang trại tin tưởng lựa chọn.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="cta" size="lg" className="bg-white text-primary hover:bg-white/90">
                Xem gói dịch vụ
              </Button>
              <Button variant="outline" size="lg" className="border-white text-gray-600  ">
                Tư vấn miễn phí
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Services;