import { Typography } from "@mui/material"
import { GridPaginationModel } from "@mui/x-data-grid"
import { HeaderLayout, QueryContainer } from "@pautena/react-design-system"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { WorkoutsService } from "../../../client"

export const Route = createFileRoute("/_layout/workouts/$id")({
  component: Workout,
})

function getWorkoutQueryOptions({ id }: { id: string }) {
  return {
    queryFn: () => WorkoutsService.readWorkout({ id }),
    queryKey: ["workouts", { id }],
  }
}

function Workout() {
  const { id } = Route.useParams()

  const { data: workout, isPending } = useQuery({
    ...getWorkoutQueryOptions({ id }),
    placeholderData: (prevData) => prevData,
  })

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
  )
}
