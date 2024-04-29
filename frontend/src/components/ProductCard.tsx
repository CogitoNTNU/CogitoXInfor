import React, { useState } from "react";
import { Product } from "../types";

interface ProductProps {
  product: Product;
}

const ProductCard: React.FC<ProductProps> = ({ product }) => {
  return (
    <div className="max-w-xs rounded overflow-hidden shadow-lg product-card max-h-100">
      <div className="h-48 w-full overflow-hidden">
        <img
          className="w-full h-full object-cover object-center"
          src={product.picture}
          alt={product.title}
        />
      </div>
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{product.title}</div>
        <p className="text-gray-700 text-base line-clamp-3">
          {product.description}
        </p>
      </div>
      <div className="px-6 py-4">
        <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">
          {product.manufacturer}
        </span>
        <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
          ${product.price.toFixed(1)}
        </span>
      </div>
    </div>
  );
};

export default ProductCard;
