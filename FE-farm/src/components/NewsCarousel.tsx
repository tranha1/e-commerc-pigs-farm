import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, ArrowRight, Newspaper, ChevronLeft, ChevronRight } from "lucide-react";
import type { NewsArticle } from "@/services/api";

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import './NewsCarousel.css';

interface NewsCarouselProps {
  articles: NewsArticle[];
  categories?: { [key: number]: string };
}

const NewsCarousel = ({ articles, categories = {} }: NewsCarouselProps) => {
  const getCategoryName = (categoryId?: number) => {
    if (!categoryId) return 'Tin tức';
    return categories[categoryId] || 'Tin tức';
  };

  const getReadTimeDisplay = (readTime?: number) => {
    if (!readTime) return 'N/A';
    return `${readTime} phút đọc`;
  };

  return (
    <div className="relative">
      <Swiper
        modules={[Navigation, Pagination, Autoplay]}
        spaceBetween={24}
        slidesPerView={1}
        breakpoints={{
          640: {
            slidesPerView: 1,
            spaceBetween: 20,
          },
          768: {
            slidesPerView: 2,
            spaceBetween: 24,
          },
          1024: {
            slidesPerView: 2,
            spaceBetween: 32,
          },
        }}
        autoplay={{
          delay: 4000,
          disableOnInteraction: false,
          pauseOnMouseEnter: true,
        }}
        pagination={{
          clickable: true,
          dynamicBullets: true,
        }}
        navigation={{
          prevEl: '.swiper-button-prev-custom',
          nextEl: '.swiper-button-next-custom',
        }}
        loop={true}
        className="news-carousel pb-12"
      >
        {articles.map((article) => (
          <SwiperSlide key={article.id}>
            <Card className="border border-border shadow-soft hover:shadow-strong transition-all duration-300 group h-full">
              <div className="aspect-video bg-gradient-to-r from-primary/10 to-accent/10 rounded-t-lg flex items-center justify-center">
                <Newspaper className="h-12 w-12 text-primary/60" />
              </div>
              <CardContent className="p-6 flex flex-col h-full">
                <div className="flex items-center gap-2 mb-3">
                  <Badge variant="secondary" className="text-xs">
                    {getCategoryName(article.category_id)}
                  </Badge>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Calendar className="h-3 w-3" />
                    <span>{new Date(article.published_at || article.created_at || '').toLocaleDateString('vi-VN')}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">•</span>
                  <span className="text-xs text-muted-foreground">{getReadTimeDisplay(article.read_time)}</span>
                </div>
                
                <h4 className="text-lg font-semibold text-foreground mb-3 group-hover:text-primary transition-colors line-clamp-2 flex-grow">
                  {article.title}
                </h4>
                
                <p className="text-muted-foreground text-sm leading-relaxed mb-4 line-clamp-3 flex-grow">
                  {article.summary}
                </p>
                
                <Button variant="ghost" size="sm" className="p-0 h-auto group-hover:text-primary mt-auto self-start">
                  Đọc thêm
                  <ArrowRight className="ml-1 h-3 w-3 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Custom Navigation Buttons */}
      <button className="swiper-button-prev-custom absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 bg-background border border-border rounded-full w-10 h-10 flex items-center justify-center hover:bg-muted transition-colors shadow-md">
        <ChevronLeft className="h-5 w-5 text-foreground" />
      </button>
      <button className="swiper-button-next-custom absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 bg-background border border-border rounded-full w-10 h-10 flex items-center justify-center hover:bg-muted transition-colors shadow-md">
        <ChevronRight className="h-5 w-5 text-foreground" />
      </button>


    </div>
  );
};

export default NewsCarousel;