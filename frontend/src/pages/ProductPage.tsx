import { useParams } from "react-router-dom";
import { Product } from "../types";
import { useEffect, useState } from "react";
import { GetProduct } from "../services/GetProduct";
import { GetRecommendations } from "../services/GetRecommentadtions";
import ProductCard from "../components/ProductCard";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import { Button, Typography, styled } from "@mui/material";
import ProductCardGrid from "../components/ProductCardGrid";

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
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  const StyledButton = styled(Button)(({ theme }) => ({
    color: theme.palette.getContrastText("#424242"),
    backgroundColor: "#424242",
    borderRadius: 50,
    boxShadow: "0 3px 5px 2px rgba(66, 66, 66, .3)",
    padding: "0 30px",
    margin: theme.spacing(1),
  }));

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 2,
      }}
    >
      <ProductCard product={product} />
      <StyledButton onClick={() => window.history.back()}>Go back</StyledButton>
      <Typography
        variant="h6"
        component="h2"
        sx={{ display: { xs: "none", sm: "block" } }}
      >
        Recommended products:
      </Typography>
      {recommendations && <ProductCardGrid products={recommendations} />}
    </Box>
  );
};

export default ProductPage;
