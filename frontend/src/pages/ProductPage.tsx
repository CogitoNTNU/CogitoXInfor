import { useParams } from "react-router-dom";
import { Product } from "../types";
import { useEffect, useState } from "react";
import { GetProduct } from "../services/GetProduct";
import { GetRecommendations } from "../services/GetRecommentadtions";
import ProductCard from "../components/ProductCard";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

const ProductPage = () => {
  const { productID } = useParams<{ productID: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [recommendations, setRecommendations] = useState<Product[] | null>(
    null
  );

  useEffect(() => {
    // Check if productID exists
    if (!productID) {
      return;
    }
    // get product
    GetProduct({ id: productID }).then((product) => {
      if (product) {
        setProduct(product);
      }
    });
    // get recommendations
    GetRecommendations({ id: productID, amount: 10 }).then(
      (recommendations) => {
        if (recommendations) {
          setRecommendations(recommendations);
        }
      }
    );
  }, [productID]);

  if (!product) {
    return (
      <Box sx={{ display: "flex" }}>
        <CircularProgress />
      </Box>
    );
  }

  return <ProductCard product={product} />;
};

export default ProductPage;
