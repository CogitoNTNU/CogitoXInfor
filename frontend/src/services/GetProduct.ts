import axios from "axios";
import type { GetProduct, Product } from "../types";
import { apiRoutes } from "../routes/routeDefinitions";

const GetProduct = async (params: GetProduct): Promise<Product | null> => {
  try {
    const response = await axios.get<Product>(`${apiRoutes.product}`, {
      params,
    });

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error("Error in getProduct");
    }
  } catch (error) {
    console.error("Error in getProduct:", error);
    return null;
  }
};

export { GetProduct };
