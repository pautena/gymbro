import { Button, Grid2, TextField } from "@mui/material";
import {
  HeaderLayout,
  useNotificationCenter,
} from "@pautena/react-design-system";
import { useQueryClient } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";
import type { WorkoutCreate } from "../../../client";
import { useCreateWorkoutMutation } from "../../../features/workouts/workouts.client";

export const Route = createFileRoute("/_layout/workouts/add")({
  component: AddWorkout,
});

function AddWorkout() {
  const navigate = Route.useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<WorkoutCreate>({
    defaultValues: {
      name: "",
    },
  });

  const mutation = useCreateWorkoutMutation({
    onSuccess: () => {
      navigate({ to: "/workouts", search: { page: 0 } });
    },
  });

  const onSubmit: SubmitHandler<WorkoutCreate> = (data) => {
    mutation.mutate(data);
  };

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
            label="date (YYYY-MM-DD)"
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
  );
}
