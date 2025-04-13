import { useNotificationCenter } from "@pautena/react-design-system";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { type WorkoutCreate, WorkoutsService } from "../../client";
import { type UseMutationArgs, handleError } from "../../utils";

interface UseGetWorkoutsQueryArgs {
  page: number;
  pageSize: number;
}

export function readWorkoutsQueryOptions({
  page,
  pageSize,
}: UseGetWorkoutsQueryArgs) {
  return {
    queryFn: async () => {
      const response = WorkoutsService.readWorkouts({
        query: {
          skip: page * pageSize,
          limit: pageSize,
        },
      });
      return (await response).data;
    },
    queryKey: ["workouts"],
  };
}

export const useReadWorkoutsQuery = (args: UseGetWorkoutsQueryArgs) => {
  return useQuery({
    ...readWorkoutsQueryOptions(args),
    placeholderData: (prevData) => prevData,
  });
};

export function getWorkoutQueryOptions({ id }: { id: string }) {
  return {
    queryFn: async () => {
      const response = await WorkoutsService.readWorkout({ path: { id } });
      return response.data;
    },
    queryKey: ["workouts", { id }],
  };
}

export const useGetWorkoutQuery = ({ id }: { id: string }) => {
  return useQuery({
    ...getWorkoutQueryOptions({ id }),
    placeholderData: (prevData) => prevData,
  });
};

export const useCreateWorkoutMutation = ({
  onSuccess = () => {},
}: UseMutationArgs = {}) => {
  const queryClient = useQueryClient();
  const { show } = useNotificationCenter();

  return useMutation({
    mutationFn: (data: WorkoutCreate) =>
      WorkoutsService.createWorkout({ body: data }),
    onSuccess: () => {
      show({
        severity: "success",
        message: "Workout created",
      });
      onSuccess();
    },
    onError: (err) => {
      handleError(err, show);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["workouts"] });
    },
  });
};
