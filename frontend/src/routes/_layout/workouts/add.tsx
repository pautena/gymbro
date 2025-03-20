import { Button, Grid2, TextField } from "@mui/material"
import {
  HeaderLayout,
  useNotificationCenter,
} from "@pautena/react-design-system"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { type SubmitHandler, useForm } from "react-hook-form"
import {
  type ApiError,
  type WorkoutCreate,
  WorkoutsService,
} from "../../../client"

export const Route = createFileRoute("/_layout/workouts/add")({
  component: AddWorkout,
})

function AddWorkout() {
  const queryClient = useQueryClient()
  const { show } = useNotificationCenter()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<WorkoutCreate>({
    defaultValues: {
      name: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: WorkoutCreate) =>
      WorkoutsService.createWorkout({ requestBody: data }),
    onSuccess: () => {
      show({
        severity: "success",
        message: "Item created",
      })
    },
    onError: (err: ApiError) => {
      show({
        severity: "error",
        message: err.message,
      })
      redirect({ to: "/workouts", search: { page: 0 }, throw: true })
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["workouts"] })
    },
  })

  const onSubmit: SubmitHandler<WorkoutCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <HeaderLayout title="Add workout" loading={isSubmitting}>
      <Grid2
        container
        spacing={2}
        component="form"
        onSubmit={handleSubmit(onSubmit)}
      >
        <Grid2 size={12}>
          <TextField
            {...register("name", { required: true })}
            label="Name"
            fullWidth
            variant="outlined"
            error={!!errors.name}
            helperText={errors.name?.message}
          />
        </Grid2>
        <Grid2 size={12}>
          <TextField
            {...register("notes", { required: true })}
            label="Notes"
            multiline
            fullWidth
            rows={4}
            variant="outlined"
            error={!!errors.notes}
            helperText={errors.notes?.message}
          />
        </Grid2>
        <Grid2 size={12}>
          <TextField
            {...register("date", { required: true })}
            label="date"
            fullWidth
            variant="outlined"
            error={!!errors.name}
            helperText={errors.name?.message}
          />
        </Grid2>
        <Grid2 size={12}>
          <Button type="submit" variant="contained">
            Save
          </Button>
        </Grid2>
      </Grid2>
    </HeaderLayout>
  )
}
