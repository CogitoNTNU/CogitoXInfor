import { useEffect, useState } from "react";
import { Product } from "../types";
import { GetProducts } from "../services/GetProducts";
import ProductCardGrid from "../components/ProductCardGrid";

const HomePage = () => {
  const [products, setProducts] = useState<Product[] | null>(null);

  useEffect(() => {
    // get products
    GetProducts({ amount: 20, search: "", offset: 0 }).then((products) => {
      if (products) {
        setProducts(products);
      }
    });
  }, []);
  return <ProductCardGrid products={products || []} />;
};

export default HomePage;
