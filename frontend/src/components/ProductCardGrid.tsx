import React from "react";
import { Product } from "../types";
import ProductCard from "./ProductCard";
import { useNavigate } from "react-router-dom";

interface ProductCardGridProps {
  products: Product[];
}

const ProductCardGrid: React.FC<ProductCardGridProps> = ({ products }) => {
  const navigate = useNavigate();

  return (
    <div className="flex gap-6  flex-wrap justify-center grid-container items-start">
      {products.map((product, index) => (
        <button key={index} onClick={() => navigate("/product/" + product.id)}>
          <ProductCard key={index} product={product} />
        </button>
      ))}
    </div>
  );
};

export default ProductCardGrid;
