import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { 
  MapPin, 
  Phone, 
  Mail, 
  Clock, 
  Send,
  MessageSquare,
  Building,
  Tractor,
  Users
} from "lucide-react";
import { useState } from "react";

const Contact = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    company: "",
    subject: "",
    message: "",
    inquiryType: "general"
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    alert("Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ phản hồi trong thời gian sớm nhất.");
    
    // Reset form
    setFormData({
      name: "",
      email: "",
      phone: "",
      company: "",
      subject: "",
      message: "",
      inquiryType: "general"
    });
    
    setIsSubmitting(false);
  };

  const contactInfo = [
    {
      icon: <Building className="h-6 w-6 text-primary" />,
      title: "Văn phòng chính",
      details: [
        "4 ngách 10/461 Ng. 461 Đ. Nguyễn Văn Linh",
        "Sài Đồng, Long Biên, Hà Nội"
      ]
    },
    {
      icon: <Tractor className="h-6 w-6 text-primary" />,
      title: "Trại hạt nhân",
      details: [
        "Hợp tác xã Metafarm",
        "Xã Việt Hoà, huyện Khoái Châu, tỉnh Hưng Yên"
      ]
    },
    {
      icon: <Building className="h-6 w-6 text-primary" />,
      title: "Trại xuất bán heo giống",
      details: [
        "Trại Metavet",
        "Xã Ba Trại, huyện Ba Vì, Hà Nội"
      ]
    }
  ];

  const contactMethods = [
    {
      icon: <Phone className="h-5 w-5 text-primary" />,
      title: "Điện thoại",
      value: "0975 885 946",
      link: "tel:0975885946"
    },
    {
      icon: <Phone className="h-5 w-5 text-primary" />,
      title: "Hotline",
      value: "0868 222 136",
      link: "tel:0868222136"
    },
    {
      icon: <Mail className="h-5 w-5 text-primary" />,
      title: "Email",
      value: "info@metafarm.vn",
      link: "mailto:info@metafarm.vn"
    },
    {
      icon: <Clock className="h-5 w-5 text-primary" />,
      title: "Giờ làm việc",
      value: "8:00 - 17:00 (T2-T7)",
      link: ""
    }
  ];

  const inquiryTypes = [
    { value: "general", label: "Tư vấn chung" },
    { value: "product", label: "Sản phẩm heo giống" },
    { value: "technical", label: "Hỗ trợ kỹ thuật" },
    { value: "partnership", label: "Hợp tác kinh doanh" },
    { value: "visit", label: "Đặt lịch tham quan" }
  ];

  return (
    <div className="min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-primary/80 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Liên hệ với chúng tôi
            </h1>
            <p className="text-xl text-primary-foreground/90 max-w-2xl mx-auto">
              Chúng tôi luôn sẵn sàng lắng nghe và hỗ trợ bạn. Hãy liên hệ ngay để được tư vấn tốt nhất!
            </p>
          </div>
        </div>
      </section>

      <main className="py-16">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-3 gap-12">
            
            {/* Contact Form */}
            <div className="lg:col-span-2">
              <Card>
                <CardContent className="p-8">
                  <div className="mb-8">
                    <h2 className="text-2xl font-bold text-foreground mb-2">
                      Gửi tin nhắn cho chúng tôi
                    </h2>
                    <p className="text-muted-foreground">
                      Điền thông tin vào form dưới đây, chúng tôi sẽ phản hồi trong vòng 24h.
                    </p>
                  </div>

                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="name">Họ và tên *</Label>
                        <Input
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleInputChange}
                          placeholder="Nhập họ và tên"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="email">Email *</Label>
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleInputChange}
                          placeholder="example@email.com"
                          required
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="phone">Số điện thoại</Label>
                        <Input
                          id="phone"
                          name="phone"
                          value={formData.phone}
                          onChange={handleInputChange}
                          placeholder="0xxx xxx xxx"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="company">Công ty/Trang trại</Label>
                        <Input
                          id="company"
                          name="company"
                          value={formData.company}
                          onChange={handleInputChange}
                          placeholder="Tên công ty hoặc trang trại"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="inquiryType">Loại yêu cầu</Label>
                      <select
                        id="inquiryType"
                        name="inquiryType"
                        value={formData.inquiryType}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                      >
                        {inquiryTypes.map((type) => (
                          <option key={type.value} value={type.value}>
                            {type.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="subject">Tiêu đề *</Label>
                      <Input
                        id="subject"
                        name="subject"
                        value={formData.subject}
                        onChange={handleInputChange}
                        placeholder="Tiêu đề tin nhắn"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="message">Nội dung tin nhắn *</Label>
                      <Textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleInputChange}
                        placeholder="Nội dung chi tiết yêu cầu của bạn..."
                        rows={6}
                        required
                      />
                    </div>

                    <Button 
                      type="submit" 
                      className="w-full md:w-auto"
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Đang gửi...
                        </>
                      ) : (
                        <>
                          <Send className="h-4 w-4 mr-2" />
                          Gửi tin nhắn
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Info Sidebar */}
            <div className="space-y-8">
              
              {/* Quick Contact */}
              <Card>
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                    <MessageSquare className="h-5 w-5 text-primary" />
                    Liên hệ nhanh
                  </h3>
                  <div className="space-y-4">
                    {contactMethods.map((method, index) => (
                      <div key={index} className="flex items-center gap-3">
                        {method.icon}
                        <div>
                          <div className="text-sm text-muted-foreground">{method.title}</div>
                          {method.link ? (
                            <a 
                              href={method.link}
                              className="text-foreground hover:text-primary transition-colors"
                            >
                              {method.value}
                            </a>
                          ) : (
                            <div className="text-foreground">{method.value}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Locations */}
              <Card>
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                    <MapPin className="h-5 w-5 text-primary" />
                    Địa điểm
                  </h3>
                  <div className="space-y-6">
                    {contactInfo.map((info, index) => (
                      <div key={index} className="flex gap-3">
                        {info.icon}
                        <div>
                          <h4 className="font-medium text-foreground mb-1">{info.title}</h4>
                          {info.details.map((detail, idx) => (
                            <p key={idx} className="text-sm text-muted-foreground">
                              {detail}
                            </p>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Service Hours */}
              <Card className="bg-gradient-to-br from-primary/10 to-accent/10 border-primary/20">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                    <Users className="h-5 w-5 text-primary" />
                    Hỗ trợ khách hàng
                  </h3>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Thứ 2 - Thứ 6:</span>
                      <span className="text-foreground font-medium">8:00 - 17:00</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Thứ 7:</span>
                      <span className="text-foreground font-medium">8:00 - 12:00</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Chủ nhật:</span>
                      <span className="text-foreground font-medium">Nghỉ</span>
                    </div>
                    <div className="border-t border-border pt-3 mt-3">
                      <p className="text-primary font-medium">Hotline 24/7: 0975 885 946</p>
                      <p className="text-muted-foreground text-xs mt-1">
                        Hỗ trợ khẩn cấp ngoài giờ làm việc
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Map Section */}
          <div className="mt-16">
            <Card>
              <CardContent className="p-0">
                <div className="bg-gradient-to-r from-primary/20 to-accent/20 p-8 text-center">
                  <h3 className="text-2xl font-bold text-foreground mb-4">
                    Bản đồ vị trí
                  </h3>
                  <p className="text-muted-foreground mb-6">
                    Ghé thăm văn phòng và trang trại của chúng tôi
                  </p>
                  
                  {/* Placeholder for map - you can integrate Google Maps or other map services */}
                  <div className="bg-muted rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center">
                      <MapPin className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground">
                        Bản đồ sẽ được hiển thị tại đây
                      </p>
                      <p className="text-sm text-muted-foreground mt-2">
                        (Tích hợp Google Maps hoặc OpenStreetMap)
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Contact;