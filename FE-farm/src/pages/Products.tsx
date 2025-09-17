import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import { useMedicines, usePigs } from "@/hooks/useApi";
import { formatCurrency } from "@/lib/utils";
import { Link } from "react-router-dom";
import { Eye } from "lucide-react";

const Products = () => {
    // Fetch data from API
    const { data: medicinesData, isLoading: medicinesLoading, error: medicinesError } = useMedicines({ published: true });
    const { data: pigsData, isLoading: pigsLoading, error: pigsError } = usePigs({ published: true });

    const renderMedicines = () => {
        if (medicinesLoading) {
            return (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[...Array(6)].map((_, index) => (
                        <Card key={index}>
                            <CardHeader>
                                <Skeleton className="h-6 w-3/4" />
                                <Skeleton className="h-4 w-1/2" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-20 w-full" />
                            </CardContent>
                        </Card>
                    ))}
                </div>
            );
        }

        if (medicinesError) {
            return (
                <Alert>
                    <AlertDescription>
                        Không thể tải dữ liệu thuốc. Vui lòng thử lại sau.
                    </AlertDescription>
                </Alert>
            );
        }

        if (!medicinesData?.data || medicinesData.data.length === 0) {
            return (
                <Alert>
                    <AlertDescription>
                        Hiện tại chưa có sản phẩm thuốc nào được công bố.
                    </AlertDescription>
                </Alert>
            );
        }

        return (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {medicinesData.data.map((medicine) => (
                    <Card key={medicine.id} className="hover:shadow-lg transition-shadow">
                        <CardHeader>
                            <CardTitle className="text-xl">{medicine.name}</CardTitle>
                            <Badge variant="outline">
                                {medicine.is_published ? 'Có sẵn' : 'Hết hàng'}
                            </Badge>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            {medicine.packaging && (
                                <div>
                                    <h4 className="font-semibold text-foreground mb-1">ĐÓNG GÓI</h4>
                                    <p className="text-sm text-muted-foreground">{medicine.packaging}</p>
                                </div>
                            )}
                            
                            <div className="space-y-2">
                                {medicine.price_unit && (
                                    <div className="flex justify-between">
                                        <span className="text-sm text-muted-foreground">Giá đơn vị:</span>
                                        <span className="font-semibold">{formatCurrency(medicine.price_unit)}</span>
                                    </div>
                                )}
                                {medicine.price_total && (
                                    <div className="flex justify-between">
                                        <span className="text-sm text-muted-foreground">Giá tổng:</span>
                                        <span className="font-semibold">{formatCurrency(medicine.price_total)}</span>
                                    </div>
                                )}
                            </div>

                            {medicine.updated_at && (
                                <div className="pt-2 border-t">
                                    <p className="text-xs text-muted-foreground">
                                        Cập nhật: {new Date(medicine.updated_at).toLocaleDateString('vi-VN')}
                                    </p>
                                </div>
                            )}

                            <div className="pt-3">
                                <Link to={`/products/medicine/${medicine.id}`}>
                                    <Button variant="outline" className="w-full" size="sm">
                                        <Eye className="h-4 w-4 mr-2" />
                                        Xem chi tiết
                                    </Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        );
    };

    const renderDynamicPigs = () => {
        if (pigsLoading) {
            return (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
                    {[...Array(3)].map((_, index) => (
                        <Card key={index}>
                            <CardHeader>
                                <Skeleton className="h-6 w-3/4" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-16 w-full" />
                            </CardContent>
                        </Card>
                    ))}
                </div>
            );
        }

        if (pigsError || !pigsData?.data || pigsData.data.length === 0) {
            return null; // Don't show error for pigs, just hide the section
        }

        return (
            <section className="mt-16">
                <h2 className="text-3xl font-semibold text-foreground mb-8 text-center">
                    SẢN PHẨM LỢN HIỆN CÓ
                </h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {pigsData.data.map((pig) => (
                        <Card key={pig.id}>
                            <CardHeader>
                                <CardTitle className="text-xl">{pig.name}</CardTitle>
                                <Badge variant={pig.is_published ? "default" : "secondary"}>
                                    {pig.is_published ? 'Có sẵn' : 'Hết hàng'}
                                </Badge>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                {pig.price && (
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm text-muted-foreground">Giá:</span>
                                        <span className="font-semibold text-lg">{formatCurrency(pig.price)}</span>
                                    </div>
                                )}
                                
                                {pig.updated_at && (
                                    <div className="pt-2 border-t">
                                        <p className="text-xs text-muted-foreground">
                                            Cập nhật: {new Date(pig.updated_at).toLocaleDateString('vi-VN')}
                                        </p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>
        );
    };

    return (
        <div className="min-h-screen bg-background">
            <Header />
            
            {/* Hero Section */}
            <section className="bg-gradient-to-r from-primary to-primary/80 text-white py-20">
                <div className="container mx-auto px-4">
                    <div className="text-center">
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            Sản phẩm Metafarm
                        </h1>
                        <p className="text-xl text-primary-foreground/90 max-w-3xl mx-auto">
                            Cung cấp đầy đủ các dòng heo giống chất lượng cao từ các quốc gia có nền chăn nuôi phát triển 
                            như Đan Mạch, Pháp, Đài Loan cùng với thuốc thú y và thiết bị chăn nuôi hiện đại.
                        </p>
                    </div>
                </div>
            </section>

            <main className="py-16">
                <div className="container mx-auto px-4">
                    <Tabs defaultValue="breeding-pigs" className="w-full">
                        <TabsList className="grid w-full grid-cols-2 mb-8">
                            <TabsTrigger value="breeding-pigs">Heo giống</TabsTrigger>
                            <TabsTrigger value="medicine">Thuốc thú y & Thiết bị</TabsTrigger>
                        </TabsList>

                    {/* Lợn giống Tab */}
                    <TabsContent value="breeding-pigs" className="space-y-16">
                        {/* Dynamic pigs from API */}
                        <section>
                            <h2 className="text-3xl font-semibold text-foreground mb-8 text-center">
                                SẢN PHẨM LỢN HIỆN CÓ
                            </h2>
                            {pigsLoading && (
                                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {[...Array(3)].map((_, index) => (
                                        <Card key={index}>
                                            <CardHeader>
                                                <Skeleton className="h-6 w-3/4" />
                                            </CardHeader>
                                            <CardContent>
                                                <Skeleton className="h-16 w-full" />
                                            </CardContent>
                                        </Card>
                                    ))}
                                </div>
                            )}
                            
                            {pigsError && (
                                <Alert>
                                    <AlertDescription>
                                        Không thể tải dữ liệu sản phẩm lợn. Vui lòng thử lại sau.
                                    </AlertDescription>
                                </Alert>
                            )}
                            
                            {!pigsLoading && !pigsError && (!pigsData?.data || pigsData.data.length === 0) && (
                                <Alert>
                                    <AlertDescription>
                                        Hiện tại chưa có sản phẩm lợn nào được công bố.
                                    </AlertDescription>
                                </Alert>
                            )}
                            
                            {!pigsLoading && !pigsError && pigsData?.data && pigsData.data.length > 0 && (
                                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {pigsData.data.map((pig) => (
                                        <Card key={pig.id} className="hover:shadow-lg transition-shadow">
                                            <CardHeader>
                                                <CardTitle className="text-xl">{pig.name}</CardTitle>
                                                <Badge variant={pig.is_published ? "default" : "secondary"}>
                                                    {pig.is_published ? 'Có sẵn' : 'Hết hàng'}
                                                </Badge>
                                            </CardHeader>
                                            <CardContent className="space-y-3">
                                                {pig.price && (
                                                    <div className="flex justify-between items-center">
                                                        <span className="text-sm text-muted-foreground">Giá:</span>
                                                        <span className="font-semibold text-lg">{formatCurrency(pig.price)}</span>
                                                    </div>
                                                )}
                                                
                                                {pig.updated_at && (
                                                    <div className="pt-2 border-t">
                                                        <p className="text-xs text-muted-foreground">
                                                            Cập nhật: {new Date(pig.updated_at).toLocaleDateString('vi-VN')}
                                                        </p>
                                                    </div>
                                                )}

                                                <div className="pt-3">
                                                    <Link to={`/products/pig/${pig.id}`}>
                                                        <Button variant="outline" className="w-full" size="sm">
                                                            <Eye className="h-4 w-4 mr-2" />
                                                            Xem chi tiết
                                                        </Button>
                                                    </Link>
                                                </div>
                                            </CardContent>
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </section>
                    </TabsContent>

                    {/* Thuốc Tab */}
                    <TabsContent value="medicine">
                        <section>
                            <h2 className="text-3xl font-semibold text-foreground mb-8 text-center">
                                THUỐC VÀ VẮC XIN
                            </h2>
                            {renderMedicines()}
                        </section>
                    </TabsContent>
                </Tabs>
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default Products;