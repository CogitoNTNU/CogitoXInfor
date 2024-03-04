import axios from "axios";
import { GetProduct, Product } from "../types";
import { apiRoutes } from "../routes/routeDefinitions";

export const GetProducts = async (
  params: GetProduct
): Promise<Product[] | null> => {
  try {
    const response = await axios.get<Product[]>(`${apiRoutes.products}`, {
      params,
    });

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error("Error in getProducts");
    }
  } catch (error) {
    console.error("Error in getGraphTraversalMethods:", error);
    return null;
  }
};
