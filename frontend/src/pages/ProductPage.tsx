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
        console.log(product);
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
    padding: "10px 30px",
    left: "3%",
    marginTop: "30px",
  }));

  // return (
  //   <div>
  //     <StyledButton onClick={() => window.history.back()}>Go back</StyledButton>

  //     <Box
  //       sx={{
  //         display: "flex",
  //         flexDirection: "column",
  //         alignItems: "center",
  //         gap: 2,
  //       }}
  //     >
  //       <ProductCard product={product} />
  //       <Typography
  //         variant="h6"
  //         component="h2"
  //         sx={{ display: { xs: "none", sm: "block" } }}
  //       >
  //         Recommended products:
  //       </Typography>
  //       {recommendations && <ProductCardGrid products={recommendations} />}
  //     </Box>
  //   </div>
  // );

  return (
    <div className="relative h-screen">
      {/* Low transparency background image */}
      <img
        className="absolute top-0 left-0 w-full h-full object-cover opacity-15"
        src={product.picture}
        alt={product.title}
      />
      <div className="relative">
        <StyledButton onClick={() => window.history.back()}>
          Go back
        </StyledButton>
        <div className="flex flex-col items-center gap-4">
          <div className="flex flex-row items-center gap-4 w-3/4">
            <img
              className="w-1/6 h-1/6 object-cover object-center"
              src={product.picture}
              alt={product.title}
            />

            <div className="flex flex-col gap-4 justify-center items-center">
              <div className="font-bold text-3xl mb-2">{product.title}</div>
              <p className="text-gray-700 text-base line-clamp-3">
                {product.description}
              </p>
              <div className="flex gap-4">
                <span className="inline-block bg-gray-200 rounded-full px-5 py-2 text-base font-semibold text-gray-700">
                  {product.manufacturer}
                </span>
                <span className="inline-block bg-gray-200 rounded-full px-5 py-2 text-base font-semibold text-gray-700">
                  ${product.price.toFixed(1)}
                </span>
              </div>
            </div>
          </div>

          {/* <ProductCard product={product} /> */}
          <h3 className="hidden sm:block text-3xl font-normal mt-6">
            Recommended products:
          </h3>
          {recommendations && (
            <div className=" mt-6">
              <ProductCardGrid products={recommendations} />{" "}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
