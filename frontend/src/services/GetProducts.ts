import axios from "axios";
import { GetProducts, Product } from "../types";
import { apiRoutes } from "../routes/routeDefinitions";

const GetProducts = async (params: GetProducts): Promise<Product[] | null> => {
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
    console.error("Error in getProducts:", error);
    return null;
  }
};

export { GetProducts };
