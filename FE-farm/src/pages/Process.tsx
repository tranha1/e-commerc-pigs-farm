import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Plane,
  Truck,
  Shield,
  Users,
  CheckCircle,
  ArrowRight,
  MapPin,
  Clock,
  Award,
  Microscope,
  Heart,
  Target,
  FileCheck,
  Stethoscope,
  TrendingUp,
  UserCheck
} from "lucide-react";

const Process = () => {
  const importProcess = [
    {
      step: 1,
      title: "Lựa chọn đối tác uy tín",
      description: "Hợp tác với các tập đoàn hàng đầu từ Đan Mạch, Pháp và Đài Loan",
      details: [
        "Axiom và Cooperl từ Pháp", 
        "Danish Genetics từ Đan Mạch",
        "Các trại giống Duroc từ Đài Loan"
      ],
      icon: <Users className="h-8 w-8 text-primary" />,
      color: "from-blue-500 to-blue-600"
    },
    {
      step: 2,
      title: "Kiểm tra chất lượng giống",
      description: "Áp dụng tiêu chuẩn nghiêm ngặt trong lựa chọn heo giống",
      details: [
        "Kiểm tra di truyền và phả hệ",
        "Đánh giá chỉ số sinh trưởng",
        "Kiểm tra sức khỏe và miễn dịch"
      ],
      icon: <Microscope className="h-8 w-8 text-primary" />,
      color: "from-green-500 to-green-600"
    },
    {
      step: 3,
      title: "Quy trình kiểm dịch",
      description: "Tuân thủ đầy đủ các quy định kiểm dịch quốc tế và trong nước",
      details: [
        "Kiểm tra sức khỏe tại nguồn",
        "Cách ly và theo dõi 30 ngày",
        "Xét nghiệm đầy đủ các bệnh"
      ],
      icon: <Shield className="h-8 w-8 text-primary" />,
      color: "from-orange-500 to-orange-600"
    },
    {
      step: 4,
      title: "Vận chuyển an toàn",
      description: "Sử dụng các phương tiện chuyên dụng đảm bảo an toàn tuyệt đối",
      details: [
        "Máy bay cargo chuyên dụng",
        "Kiểm soát nhiệt độ và thông gió",
        "Đội ngũ thú y đi cùng"
      ],
      icon: <Plane className="h-8 w-8 text-primary" />,
      color: "from-purple-500 to-purple-600"
    },
    {
      step: 5,
      title: "Cách ly và thích nghi",
      description: "Cho heo giống thích nghi với điều kiện khí hậu Việt Nam",
      details: [
        "Cách ly 45 ngày tại trại hạt nhân",
        "Theo dõi sức khỏe 24/7",
        "Chế độ dinh dưỡng chuyên biệt"
      ],
      icon: <Heart className="h-8 w-8 text-primary" />,
      color: "from-red-500 to-red-600"
    },
    {
      step: 6,
      title: "Phân phối đến khách hàng",
      description: "Giao hàng và hỗ trợ kỹ thuật tận nơi cho khách hàng",
      details: [
        "Vận chuyển bằng xe chuyên dụng",
        "Hướng dẫn kỹ thuật chăn nuôi",
        "Hỗ trợ sau bán hàng"
      ],
      icon: <Truck className="h-8 w-8 text-primary" />,
      color: "from-indigo-500 to-indigo-600"
    }
  ];

  const breedingProcess = [
    {
      title: "Chọn giống bố mẹ",
      description: "Lựa chọn heo bố mẹ có phả hệ rõ ràng, chỉ số di truyền cao",
      icon: <Target className="h-6 w-6 text-primary" />
    },
    {
      title: "Phối giống khoa học",
      description: "Áp dụng kỹ thuật phối giống hiện đại, theo dõi chu kỳ sinh sản",
      icon: <Microscope className="h-6 w-6 text-primary" />
    },
    {
      title: "Chăm sóc nái mang thai",
      description: "Chế độ dinh dưỡng đặc biệt, theo dõi sức khỏe định kỳ",
      icon: <Heart className="h-6 w-6 text-primary" />
    },
    {
      title: "Sinh đẻ và nuôi con",
      description: "Hỗ trợ sinh đẻ, chăm sóc heo con từ những ngày đầu",
      icon: <UserCheck className="h-6 w-6 text-primary" />
    },
    {
      title: "Theo dõi phát triển",
      description: "Ghi nhận chỉ số tăng trọng, đánh giá chất lượng giống",
      icon: <TrendingUp className="h-6 w-6 text-primary" />
    },
    {
      title: "Chứng nhận chất lượng",
      description: "Cấp giấy chứng nhận giống, hồ sơ phả hệ đầy đủ",
      icon: <Award className="h-6 w-6 text-primary" />
    }
  ];

  const qualityStandards = [
    {
      title: "Kiểm soát di truyền",
      description: "100% heo giống có phả hệ rõ ràng, chỉ số di truyền được kiểm định",
      percentage: "100%",
      icon: <FileCheck className="h-5 w-5 text-white" />
    },
    {
      title: "Kiểm tra sức khỏe",
      description: "Xét nghiệm đầy đủ các bệnh truyền nhiễm, đảm bảo sức khỏe tuyệt đối",
      percentage: "100%",
      icon: <Stethoscope className="h-5 w-5 text-white" />
    },
    {
      title: "Tỷ lệ thành công",
      description: "Tỷ lệ heo giống thích nghi thành công với điều kiện Việt Nam",
      percentage: "98%",
      icon: <CheckCircle className="h-5 w-5 text-white" />
    },
    {
      title: "Hỗ trợ kỹ thuật",
      description: "Đội ngũ chuyên gia thú y hỗ trợ khách hàng 24/7",
      percentage: "24/7",
      icon: <Users className="h-5 w-5 text-white" />
    }
  ];

  const facilities = [
    {
      name: "Trại hạt nhân Hưng Yên",
      location: "Xã Việt Hoà, huyện Khoái Châu, tỉnh Hưng Yên",
      capacity: "500 nái sinh sản",
      speciality: "Giống Duroc Đài Loan, GGP, GP",
      features: ["Hệ thống chuồng trại hiện đại", "Kiểm soát môi trường tự động", "Phòng thí nghiệm tại chỗ"]
    },
    {
      name: "Trại xuất bán Ba Vì",
      location: "Xã Ba Trại, huyện Ba Vì, Hà Nội", 
      capacity: "1000 con/tháng",
      speciality: "PS, GP ready-to-breed",
      features: ["Khu cách ly chuyên biệt", "Hệ thống vận chuyển", "Đào tạo khách hàng"]
    },
    {
      name: "Văn phòng điều hành",
      location: "Long Biên, Hà Nội",
      capacity: "Điều phối toàn quốc",
      speciality: "Quản lý và hỗ trợ",
      features: ["Trung tâm điều hành", "Hỗ trợ kỹ thuật", "Đào tạo chuyên nghiệp"]
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
              Quy trình sản xuất & phân phối
            </h1>
            <p className="text-xl text-primary-foreground/90 max-w-3xl mx-auto">
              Metafarm áp dụng quy trình khoa học, từ khâu lựa chọn giống, nhập khẩu, 
              chăn nuôi đến phân phối, đảm bảo chất lượng cao nhất cho khách hàng
            </p>
          </div>
        </div>
      </section>

      <main className="py-16">
        <div className="container mx-auto px-4">
          
          {/* Import Process */}
          <section className="mb-20">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Quy trình nhập khẩu heo giống
              </h2>
              <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
                Từ việc lựa chọn đối tác uy tín đến giao hàng tận nơi, 
                mỗi bước đều được thực hiện với tiêu chuẩn cao nhất
              </p>
            </div>

            <div className="space-y-8">
              {importProcess.map((step, index) => (
                <Card key={index} className="overflow-hidden border-l-4 border-l-primary">
                  <CardContent className="p-0">
                    <div className="grid md:grid-cols-4 gap-0">
                      {/* Step Number & Icon */}
                      <div className={`bg-gradient-to-br ${step.color} text-white p-8 flex flex-col items-center justify-center`}>
                        <div className="text-3xl font-bold mb-2">0{step.step}</div>
                        {step.icon}
                      </div>
                      
                      {/* Content */}
                      <div className="md:col-span-3 p-8">
                        <div className="flex items-center gap-3 mb-4">
                          <h3 className="text-xl font-bold text-foreground">{step.title}</h3>
                          <Badge variant="secondary">Bước {step.step}</Badge>
                        </div>
                        <p className="text-muted-foreground mb-4 text-lg">
                          {step.description}
                        </p>
                        <div className="grid md:grid-cols-3 gap-3">
                          {step.details.map((detail, idx) => (
                            <div key={idx} className="flex items-center gap-2 text-sm">
                              <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                              <span className="text-foreground">{detail}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Quality Standards */}
          <section className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Tiêu chuẩn chất lượng
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Cam kết về chất lượng được thể hiện qua các chỉ số cụ thể
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {qualityStandards.map((standard, index) => (
                <Card key={index} className="overflow-hidden">
                  <CardContent className="p-0">
                    <div className="bg-gradient-to-br from-primary to-primary/80 text-white p-6 text-center">
                      <div className="flex justify-center mb-4">
                        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                          {standard.icon}
                        </div>
                      </div>
                      <div className="text-3xl font-bold mb-2">{standard.percentage}</div>
                      <h3 className="font-semibold text-lg">{standard.title}</h3>
                    </div>
                    <div className="p-6">
                      <p className="text-muted-foreground text-sm">
                        {standard.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Breeding Process */}
          <section className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Quy trình chăn nuôi tại trại
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Từ khâu phối giống đến nuôi dưỡng, mỗi giai đoạn đều được chăm sóc tỉ mỉ
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {breedingProcess.map((process, index) => (
                <Card key={index} className="border border-border shadow-soft hover:shadow-strong transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                        {process.icon}
                      </div>
                      <h3 className="font-semibold text-lg text-foreground">
                        {process.title}
                      </h3>
                    </div>
                    <p className="text-muted-foreground">
                      {process.description}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Facilities */}
          <section className="mb-20">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Hệ thống cơ sở vật chất
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Cơ sở hạ tầng hiện đại đảm bảo chất lượng sản phẩm và dịch vụ
              </p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
              {facilities.map((facility, index) => (
                <Card key={index} className="border border-border shadow-soft">
                  <CardContent className="p-8">
                    <div className="text-center mb-6">
                      <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                        <MapPin className="h-8 w-8 text-primary" />
                      </div>
                      <h3 className="text-xl font-bold text-foreground mb-2">
                        {facility.name}
                      </h3>
                      <p className="text-muted-foreground text-sm mb-4">
                        {facility.location}
                      </p>
                      <div className="flex justify-center gap-4 mb-4">
                        <Badge variant="secondary">{facility.capacity}</Badge>
                        <Badge variant="outline">{facility.speciality}</Badge>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      {facility.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm text-foreground">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Timeline */}
          <section className="mb-20">
            <Card className="bg-gradient-to-r from-primary/10 to-accent/10 border-primary/20">
              <CardContent className="p-8">
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-foreground mb-4">
                    Thời gian thực hiện dự kiến
                  </h2>
                  <p className="text-muted-foreground">
                    Từ đặt hàng đến giao heo giống tận nơi
                  </p>
                </div>

                <div className="grid md:grid-cols-4 gap-6 text-center">
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold mb-3">
                      1
                    </div>
                    <h4 className="font-semibold text-foreground mb-2">Đặt hàng</h4>
                    <p className="text-sm text-muted-foreground">Ngay khi xác nhận</p>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold mb-3">
                      2
                    </div>
                    <h4 className="font-semibold text-foreground mb-2">Chuẩn bị</h4>
                    <p className="text-sm text-muted-foreground">15-30 ngày</p>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold mb-3">
                      3
                    </div>
                    <h4 className="font-semibold text-foreground mb-2">Vận chuyển</h4>
                    <p className="text-sm text-muted-foreground">3-7 ngày</p>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center text-white font-bold mb-3">
                      ✓
                    </div>
                    <h4 className="font-semibold text-foreground mb-2">Giao hàng</h4>
                    <p className="text-sm text-muted-foreground">Tận nơi</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          {/* CTA Section */}
          <section className="text-center">
            <Card className="bg-gradient-to-r from-primary to-primary/80 text-white border-0">
              <CardContent className="p-12">
                <h2 className="text-3xl font-bold mb-4">
                  Sẵn sàng bắt đầu dự án của bạn?
                </h2>
                <p className="text-xl text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
                  Liên hệ với chúng tôi để được tư vấn chi tiết về quy trình 
                  và nhận báo giá phù hợp nhất
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button variant="outline" size="lg" className="bg-white text-primary border-white hover:bg-white/90">
                    <Clock className="h-5 w-5 mr-2" />
                    Đặt lịch tham quan
                  </Button>
                  <Button variant="cta" size="lg" className="bg-accent text-white hover:bg-accent/90">
                    <ArrowRight className="h-5 w-5 mr-2" />
                    Yêu cầu báo giá
                  </Button>
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

export default Process;