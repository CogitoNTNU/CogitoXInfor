import { useParams } from "react-router-dom";
import { Product } from "../types";
import { useEffect, useState } from "react";
import { GetProducts } from "../services/GetProducts";
import { GetRecommendations } from "../services/GetRecommentadtions";

const ProductPage = () => {
  const { productID } = useParams<{ productID: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [recommendations, setRecommendations] = useState<Product[] | null>(
    null
  );

  useEffect(() => {
    // get product
    // get recommendations
  }, [productID]);

  return <h1> Products</h1>;
};

export default ProductPage;
