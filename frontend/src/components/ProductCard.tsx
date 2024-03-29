import React, { useState } from "react";
import { Product } from "../types";

interface ProductProps {
  product: Product;
}

const ProductCard: React.FC<ProductProps> = ({ product }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  const renderDescription = () => {
    if (showFullDescription || product.description.split(".").length <= 3) {
      return product.description;
    } else {
      const truncatedDescription =
        product.description.split(".").slice(0, 2).join(".") + ".";
      return truncatedDescription;
    }
  };

  return (
    <div
      className="max-w-xs rounded overflow-hidden shadow-lg product-card"
      onMouseEnter={() => setShowFullDescription(true)}
      onMouseLeave={() => setShowFullDescription(false)}
    >
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{product.title}</div>
        <p className="text-gray-700 text-base">
          {renderDescription()}
          {!showFullDescription &&
            product.description.split(".").length > 1 && (
              <span className="text-blue-500 cursor-pointer">
                {" "}
                ... (hover over the card to read more)
              </span>
            )}
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
