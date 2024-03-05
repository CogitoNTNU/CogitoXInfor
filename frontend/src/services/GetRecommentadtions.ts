import axios from "axios";
import { Product, RecommendationFormat } from "../types";
import { apiRoutes } from "../routes/routeDefinitions";

export const GetRecommendations = async (
  params: RecommendationFormat
): Promise<Product[] | null> => {
  try {
    const response = await axios.get<Product[]>(
      `${apiRoutes.recommendations}`,
      {
        params,
      }
    );

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error("Error in getRecommendations");
    }
  } catch (error) {
    console.error("Error in getRecommendations:", error);
    return null;
  }
};
