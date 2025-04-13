import { Typography } from "@mui/material";
import { HeaderLayout } from "@pautena/react-design-system";
import { createFileRoute } from "@tanstack/react-router";
import { useGetWorkoutQuery } from "../../../features/workouts/workouts.client";

export const Route = createFileRoute("/_layout/workouts/$id")({
  component: Workout,
});

function Workout() {
  const { id } = Route.useParams();

  const { data: workout, isPending } = useGetWorkoutQuery({ id });

  return (
    <HeaderLayout
      loading={isPending}
      title={workout?.name || ""}
      slotProps={{
        header: {
          breadcrumbs: [
            { id: "workouts", text: "Workouts", link: "/workouts" },
            {
              id: "detail",
              text: workout?.name || "",
              link: `/workouts/${id}`,
            },
          ],
        },
      }}
    >
      <Typography>{JSON.stringify(workout)}</Typography>
    </HeaderLayout>
  );
}
