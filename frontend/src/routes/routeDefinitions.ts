const baseAPIUrl: string = "http://localhost:8000/api/";

const apiRoutes = {
  products: `${baseAPIUrl}/products`,
  product: `${baseAPIUrl}/product`,
  recommendations: `${baseAPIUrl}/recommendations`,
};

export { apiRoutes };
