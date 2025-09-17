import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Users,
  Phone,
  GraduationCap,
  Stethoscope,
  TrendingUp,
  ShieldCheck,
  Clock,
  CheckCircle,
  ArrowRight,
  Star,
  MapPin,
  Calendar,
  BookOpen,
  Microscope,
  Heart,
  Award,
  Zap,
  MessageSquare
} from "lucide-react";

const Services = () => {
  const mainServices = [
    {
      id: "consulting",
      title: "Tư vấn di truyền & chọn giống",
      description: "Hỗ trợ khách hàng lựa chọn giống phù hợp với mục tiêu sản xuất và điều kiện trang trại",
      icon: <Users className="h-12 w-12 text-primary" />,
      features: [
        "Tư vấn lựa chọn dòng giống phù hợp",
        "Thiết kế chương trình lai tạo",
        "Đánh giá hiệu quả kinh tế",
        "Hỗ trợ lập kế hoạch sản xuất"
      ],
      price: "Miễn phí tư vấn cơ bản",
      duration: "1-2 giờ",
      availability: "24/7 hotline",
      color: "from-blue-500 to-blue-600"
    },
    {
      id: "veterinary",
      title: "Hỗ trợ thú y & sức khỏe",
      description: "Đội ngũ bác sĩ thú y giàu kinh nghiệm hỗ trợ chăm sóc sức khỏe đàn heo",
      icon: <Stethoscope className="h-12 w-12 text-primary" />,
      features: [
        "Khám chữa bệnh tại trang trại",
        "Tư vấn chương trình phòng bệnh",
        "Hỗ trợ cấp cứu 24/7",
        "Quản lý sức khỏe đàn giống"
      ],
      price: "Theo dịch vụ",
      duration: "Theo yêu cầu",
      availability: "24/7 khẩn cấp",
      color: "from-green-500 to-green-600"
    },
    {
      id: "training",
      title: "Đào tạo kỹ thuật chăn nuôi",
      description: "Chương trình đào tạo toàn diện về kỹ thuật chăn nuôi heo hiện đại",
      icon: <GraduationCap className="h-12 w-12 text-primary" />,
      features: [
        "Khóa học kỹ thuật chăn nuôi",
        "Đào tạo quản lý trang trại",
        "Workshop chuyên sâu",
        "Cấp chứng chỉ hoàn thành"
      ],
      price: "1,500,000 - 5,000,000 VNĐ",
      duration: "1-5 ngày",
      availability: "Theo lịch",
      color: "from-purple-500 to-purple-600"
    },
    {
      id: "technical",
      title: "Hỗ trợ kỹ thuật tại trang trại",
      description: "Đội ngũ kỹ thuật viên hỗ trợ triển khai và vận hành trang trại",
      icon: <TrendingUp className="h-12 w-12 text-primary" />,
      features: [
        "Thiết kế layout trang trại",
        "Hỗ trợ vận hành chuồng trại",
        "Tối ưu hóa quy trình sản xuất",
        "Theo dõi chỉ số sản xuất"
      ],
      price: "500,000 - 2,000,000 VNĐ/ngày",
      duration: "1 ngày - nhiều tháng",
      availability: "Linh hoạt",
      color: "from-orange-500 to-orange-600"
    },
    {
      id: "guarantee",
      title: "Bảo hành & hậu mãi",
      description: "Cam kết bảo hành chất lượng giống và hỗ trợ sau bán hàng",
      icon: <ShieldCheck className="h-12 w-12 text-primary" />,
      features: [
        "Bảo hành 6 tháng đầu",
        "Thay thế miễn phí nếu lỗi",
        "Hỗ trợ kỹ thuật suốt đời",
        "Chính sách hoàn tiền"
      ],
      price: "Miễn phí",
      duration: "6-12 tháng",
      availability: "Trong giờ hành chính",
      color: "from-red-500 to-red-600"
    },
    {
      id: "logistics",
      title: "Vận chuyển & giao hàng",
      description: "Dịch vụ vận chuyển chuyên nghiệp đảm bảo an toàn cho heo giống",
      icon: <Clock className="h-12 w-12 text-primary" />,
      features: [
        "Xe vận chuyển chuyên dụng",
        "Kiểm soát nhiệt độ, thông gió",
        "Bảo hiểm hàng hóa",
        "Giao hàng tận trang trại"
      ],
      price: "10,000 - 50,000 VNĐ/km",
      duration: "Theo khoảng cách",
      availability: "Toàn quốc",
      color: "from-indigo-500 to-indigo-600"
    }
  ];

  const supportPackages = [
    {
      name: "Gói Cơ bản",
      price: "Miễn phí",
      period: "3 tháng",
      description: "Phù hợp cho trang trại nhỏ, lần đầu mua heo giống",
      features: [
        "Tư vấn chọn giống",
        "Hướng dẫn chăm sóc cơ bản",
        "Hotline hỗ trợ",
        "Bảo hành 3 tháng"
      ],
      popular: false,
      color: "border-border"
    },
    {
      name: "Gói Tiêu chuẩn",
      price: "2,000,000 VNĐ",
      period: "6 tháng",
      description: "Lý tưởng cho trang trại quy mô trung bình",
      features: [
        "Tất cả dịch vụ Gói Cơ bản",
        "Thăm khám định kỳ 2 tháng/lần",
        "Đào tạo kỹ thuật chăn nuôi",
        "Hỗ trợ kỹ thuật 24/7",
        "Bảo hành 6 tháng"
      ],
      popular: true,
      color: "border-primary"
    },
    {
      name: "Gói Cao cấp",
      price: "5,000,000 VNĐ",
      period: "12 tháng",
      description: "Dành cho trang trại lớn và các dự án đầu tư",
      features: [
        "Tất cả dịch vụ Gói Tiêu chuẩn",
        "Chuyên gia thú y riêng",
        "Thiết kế quy trình sản xuất",
        "Báo cáo hiệu quả hàng tháng",
        "Ưu tiên vận chuyển",
        "Bảo hành 12 tháng"
      ],
      popular: false,
      color: "border-accent"
    }
  ];

  const trainingPrograms = [
    {
      title: "Kỹ thuật chăn nuôi heo cơ bản",
      duration: "2 ngày",
      level: "Cơ bản",
      participants: "15-20 người",
      content: [
        "Giới thiệu các giống heo",
        "Kỹ thuật chăm sóc hàng ngày",
        "Dinh dưỡng và cho ăn",
        "Phòng chống dịch bệnh"
      ],
      price: "1,500,000 VNĐ/người"
    },
    {
      title: "Quản lý trang trại heo hiện đại",
      duration: "3 ngày",
      level: "Nâng cao",
      participants: "10-15 người",
      content: [
        "Thiết kế và xây dựng trang trại",
        "Quản lý sản xuất và chi phí",
        "Công nghệ trong chăn nuôi",
        "Marketing và bán hàng"
      ],
      price: "3,000,000 VNĐ/người"
    },
    {
      title: "Chương trình lai tạo và di truyền",
      duration: "5 ngày",
      level: "Chuyên sâu",
      participants: "8-12 người",
      content: [
        "Nguyên lý di truyền ứng dụng",
        "Thiết kế chương trình lai",
        "Đánh giá và chọn lọc giống",
        "Thực hành tại trang trại"
      ],
      price: "5,000,000 VNĐ/người"
    }
  ];

  const testimonials = [
    {
      name: "Anh Nguyễn Văn A",
      company: "Trang trại ABC, Đồng Nai",
      content: "Dịch vụ tư vấn của Metafarm rất chuyên nghiệp. Sau 6 tháng áp dụng, hiệu quả kinh tế trang trại tôi tăng 30%.",
      rating: 5,
      service: "Tư vấn kỹ thuật"
    },
    {
      name: "Chị Trần Thị B",
      company: "HTX Chăn nuôi XYZ, Long An",
      content: "Khóa đào tạo rất bổ ích, giúp chúng tôi nâng cao kỹ năng và hiệu quả chăn nuôi đáng kể.",
      rating: 5,
      service: "Đào tạo"
    },
    {
      name: "Anh Lê Văn C",
      company: "Công ty DEF, Bình Dương",
      content: "Hỗ trợ 24/7 rất tốt, khi có vấn đề về sức khỏe đàn heo, đội ngũ kỹ thuật đến ngay.",
      rating: 5,
      service: "Hỗ trợ thú y"
    }
  ];

  return (
    <div className="min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-primary/80 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Dịch vụ chuyên nghiệp
            </h1>
            <p className="text-xl text-primary-foreground/90 max-w-3xl mx-auto">
              Metafarm cung cấp giải pháp toàn diện từ tư vấn, đào tạo đến hỗ trợ kỹ thuật, 
              đồng hành cùng khách hàng thành công trong chăn nuôi
            </p>
          </div>
        </div>
      </section>

      <main className="py-16">
        <div className="container mx-auto px-4">
          
          {/* Main Services */}
          <section className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Dịch vụ chính
              </h2>
              <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
                Từ tư vấn chọn giống đến hỗ trợ kỹ thuật, chúng tôi cung cấp đầy đủ các dịch vụ 
                cần thiết cho thành công của trang trại
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {mainServices.map((service) => (
                <Card key={service.id} className="overflow-hidden border border-border shadow-soft hover:shadow-strong transition-all duration-300 group">
                  <CardContent className="p-0">
                    <div className={`bg-gradient-to-br ${service.color} text-white p-6 text-center`}>
                      <div className="flex justify-center mb-4">
                        {service.icon}
                      </div>
                      <h3 className="text-xl font-bold mb-2">{service.title}</h3>
                    </div>
                    
                    <div className="p-6">
                      <p className="text-muted-foreground mb-4">
                        {service.description}
                      </p>
                      
                      <div className="space-y-2 mb-6">
                        {service.features.map((feature, idx) => (
                          <div key={idx} className="flex items-center gap-2">
                            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                            <span className="text-sm text-foreground">{feature}</span>
                          </div>
                        ))}
                      </div>
                      
                      <div className="space-y-3 mb-6">
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Giá:</span>
                          <span className="font-medium text-foreground">{service.price}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Thời gian:</span>
                          <span className="font-medium text-foreground">{service.duration}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-muted-foreground">Sẵn có:</span>
                          <span className="font-medium text-foreground">{service.availability}</span>
                        </div>
                      </div>
                      
                      <Button className="w-full group-hover:bg-primary/90 transition-colors">
                        Đặt dịch vụ ngay
                        <ArrowRight className="h-4 w-4 ml-2" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Support Packages */}
          <section className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Gói hỗ trợ toàn diện
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Lựa chọn gói dịch vụ phù hợp với quy mô và nhu cầu của trang trại
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {supportPackages.map((pkg, index) => (
                <Card key={index} className={`relative overflow-hidden ${pkg.color} ${pkg.popular ? 'ring-2 ring-primary shadow-xl scale-105' : 'shadow-soft'}`}>
                  {pkg.popular && (
                    <div className="absolute top-0 right-0 bg-primary text-white px-4 py-1 text-sm font-medium">
                      Phổ biến
                    </div>
                  )}
                  <CardContent className="p-8">
                    <div className="text-center mb-6">
                      <h3 className="text-2xl font-bold text-foreground mb-2">{pkg.name}</h3>
                      <div className="text-3xl font-bold text-primary mb-1">{pkg.price}</div>
                      <div className="text-muted-foreground">/{pkg.period}</div>
                    </div>
                    
                    <p className="text-muted-foreground text-center mb-6">
                      {pkg.description}
                    </p>
                    
                    <div className="space-y-3 mb-8">
                      {pkg.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center gap-3">
                          <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                          <span className="text-foreground">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Button 
                      className={`w-full ${pkg.popular ? 'bg-primary hover:bg-primary/90' : 'variant-outline'}`}
                      variant={pkg.popular ? "default" : "outline"}
                    >
                      Chọn gói này
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Training Programs */}
          <section className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Chương trình đào tạo
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Nâng cao kiến thức và kỹ năng chăn nuôi với các khóa học chuyên nghiệp
              </p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
              {trainingPrograms.map((program, index) => (
                <Card key={index} className="border border-border shadow-soft">
                  <CardContent className="p-8">
                    <div className="flex items-center gap-3 mb-4">
                      <GraduationCap className="h-8 w-8 text-primary" />
                      <div>
                        <h3 className="text-lg font-bold text-foreground">{program.title}</h3>
                        <div className="flex gap-2 mt-1">
                          <Badge variant="secondary">{program.duration}</Badge>
                          <Badge variant="outline">{program.level}</Badge>
                        </div>
                      </div>
                    </div>
                    
                    <div className="space-y-3 mb-6">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Số học viên:</span>
                        <span className="font-medium text-foreground">{program.participants}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Học phí:</span>
                        <span className="font-medium text-primary">{program.price}</span>
                      </div>
                    </div>
                    
                    <div className="mb-6">
                      <h4 className="font-semibold text-foreground mb-3">Nội dung khóa học:</h4>
                      <div className="space-y-2">
                        {program.content.map((item, idx) => (
                          <div key={idx} className="flex items-center gap-2">
                            <BookOpen className="h-4 w-4 text-primary flex-shrink-0" />
                            <span className="text-sm text-foreground">{item}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <Button variant="outline" className="w-full">
                      <Calendar className="h-4 w-4 mr-2" />
                      Đăng ký khóa học
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Testimonials */}
          <section className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Khách hàng nói gì về chúng tôi
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Phản hồi chân thực từ các khách hàng đã sử dụng dịch vụ của Metafarm
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <Card key={index} className="border border-border shadow-soft">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-1 mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                    
                    <p className="text-muted-foreground mb-4 italic">
                      "{testimonial.content}"
                    </p>
                    
                    <div className="border-t border-border pt-4">
                      <div className="font-semibold text-foreground">{testimonial.name}</div>
                      <div className="text-sm text-muted-foreground">{testimonial.company}</div>
                      <Badge variant="secondary" className="mt-2 text-xs">
                        {testimonial.service}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* CTA Section */}
          <section className="text-center">
            <Card className="bg-gradient-to-r from-primary to-primary/80 text-white border-0">
              <CardContent className="p-12">
                <div className="flex justify-center mb-6">
                  <MessageSquare className="h-16 w-16 text-white" />
                </div>
                <h2 className="text-3xl font-bold mb-4">
                  Cần tư vấn dịch vụ phù hợp?
                </h2>
                <p className="text-xl text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
                  Liên hệ với chuyên gia của chúng tôi để được tư vấn miễn phí 
                  và lựa chọn dịch vụ phù hợp nhất
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button variant="outline" size="lg" className="bg-white text-primary border-white hover:bg-white/90">
                    <Phone className="h-5 w-5 mr-2" />
                    Gọi ngay: 0975 885 946
                  </Button>
                  <Button variant="cta" size="lg" className="bg-accent text-white hover:bg-accent/90">
                    <ArrowRight className="h-5 w-5 mr-2" />
                    Đặt lịch tư vấn
                  </Button>
                </div>
                
                <div className="mt-8 grid md:grid-cols-3 gap-6 text-center">
                  <div>
                    <Zap className="h-8 w-8 text-white mx-auto mb-2" />
                    <div className="font-semibold">Phản hồi nhanh</div>
                    <div className="text-sm text-primary-foreground/80">Trong vòng 30 phút</div>
                  </div>
                  <div>
                    <Award className="h-8 w-8 text-white mx-auto mb-2" />
                    <div className="font-semibold">Chuyên gia giàu kinh nghiệm</div>
                    <div className="text-sm text-primary-foreground/80">10+ năm trong ngành</div>
                  </div>
                  <div>
                    <Heart className="h-8 w-8 text-white mx-auto mb-2" />
                    <div className="font-semibold">Cam kết chất lượng</div>
                    <div className="text-sm text-primary-foreground/80">Hài lòng 100%</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Services;