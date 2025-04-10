import { useQuery, useQueryClient } from "@tanstack/react-query"
import { Outlet, createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"
import { z } from "zod"

import {
  DataGrid,
  type GridColDef,
  type GridPaginationModel,
  type GridRowParams,
} from "@mui/x-data-grid"
import { HeaderLayout } from "@pautena/react-design-system"
import { type WorkoutPublic, WorkoutsService } from "../../../client"

const PAGE_SIZE = 5
const workoutsSearchSchema = z.object({
  page: z.number().optional().default(0),
})

export const Route = createFileRoute("/_layout/workouts/")({
  component: Workouts,
  validateSearch: (search) => workoutsSearchSchema.parse(search),
})

function getWorkoutsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      WorkoutsService.readWorkouts({
        skip: page * PAGE_SIZE,
        limit: PAGE_SIZE,
      }),
    queryKey: ["workouts", { page }],
  }
}

function Workouts() {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const handlePaginationModelChange = (paginationModel: GridPaginationModel) =>
    navigate({ search: (prev) => ({ ...prev, page: paginationModel.page }) })

  const {
    data: workouts,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getWorkoutsQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && workouts?.data.length === PAGE_SIZE

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getWorkoutsQueryOptions({ page: page + 1 }))
    }
  }, [page, queryClient, hasNextPage])

  const columns: GridColDef<WorkoutPublic>[] = [
    {
      field: "id",
      width: 350,
    },
    {
      field: "name",
      width: 200,
    },
    {
      field: "date",
      width: 200,
    },
  ]

  return (
    <HeaderLayout
      title="Workouts"
      slotProps={{
        header: {
          actions: [{ id: "add", text: "New Workout", href: "/workouts/add" }],
        },
      }}
    >
      <DataGrid
        columns={columns}
        loading={isPending}
        paginationMode="server"
        rows={workouts?.data || []}
        rowCount={workouts?.count || 0}
        onRowClick={({ row: { id } }: GridRowParams<WorkoutPublic>) =>
          navigate({ to: "/workouts/$id", params: { id } })
        }
        pageSizeOptions={[PAGE_SIZE]}
        paginationModel={{ page: page, pageSize: PAGE_SIZE }}
        onPaginationModelChange={handlePaginationModelChange}
        sx={{
          ".MuiDataGrid-row": { cursor: "pointer" },
        }}
      />
    </HeaderLayout>
  )
}
