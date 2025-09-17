import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle } from "lucide-react";
import { useTranslation } from "react-i18next";
import heroImage from "@/assets/hero-farm.jpg";

const Hero = () => {
  const { t } = useTranslation();
  
  const features = [
    "Nhập khẩu heo giống GGP, GP, PS từ Đan Mạch, Pháp, Đài Loan",
    "Quy trình kiểm dịch nghiêm ngặt", 
    "Đối tác uy tín: Axiom, Cooperl, Danish Genetics",
    "Hỗ trợ kỹ thuật 24/7"
  ];

  return (
    <section className="relative min-h-[80vh] flex items-center">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url(${heroImage})`
        }}
      />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-white space-y-8">
            <div className="space-y-4">
              <span className="inline-block px-4 py-2 bg-primary/20 backdrop-blur-sm text-white rounded-full text-sm font-medium">
                Tăng trưởng 400% | Phủ sóng 63 tỉnh thành
              </span>
              <h1 className="text-4xl md:text-6xl font-bold leading-tight">
                Metafarm
                <span className="text-accent block">Heo Giống Chất Lượng Cao</span>
              </h1>
              <p className="text-xl text-gray-200 leading-relaxed">
                Công ty trẻ chuyên chăn nuôi heo, nhập khẩu và phân phối heo giống từ các quốc gia 
                có ngành chăn nuôi phát triển. Cam kết cung cấp những con giống chất lượng cao nhất.
              </p>
            </div>

            {/* Features List */}
            <div className="grid grid-cols-2 gap-4">
              {features.map((feature, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <CheckCircle className="h-5 w-5 text-accent flex-shrink-0" />
                  <span className="text-sm text-gray-200">{feature}</span>
                </div>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button variant="hero" size="lg" className="group">
                Yêu cầu báo giá ngay
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="outline" size="lg" className="border-white text-gray-600  text-foreground">
                {t("common.learn_more")}
              </Button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-8 border-t border-white/20">
              <div className="text-center">
                <div className="text-3xl font-bold text-accent">400%</div>
                <div className="text-sm text-gray-300">Tăng trưởng 2021-2024</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-accent">63</div>
                <div className="text-sm text-gray-300">Tỉnh thành phủ sóng</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-accent">1000+</div>
                <div className="text-sm text-gray-300">Đơn vị tin cậy</div>
              </div>
            </div>
          </div>

          {/* Right side - Can add additional content or keep for visual balance */}
          <div className="lg:block hidden">
            {/* This space can be used for additional visual elements if needed */}
          </div>
        </div>
      </div>

      {/* Floating shapes for visual interest */}
      <div className="absolute top-20 right-10 w-20 h-20 bg-primary/10 rounded-full blur-xl animate-pulse" />
      <div className="absolute bottom-20 left-10 w-32 h-32 bg-accent/10 rounded-full blur-xl animate-pulse" style={{ animationDelay: '2s' }} />
    </section>
  );
};

export default Hero;
