import React from "react";
import { Product } from "../types";
import ProductCard from "./ProductCard";

interface ProductCardGridProps {
  products: Product[];
}

const ProductCardGrid: React.FC<ProductCardGridProps> = ({ products }) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product, index) => (
        <ProductCard key={index} product={product} />
      ))}
    </div>
  );
};

export default ProductCardGrid;
