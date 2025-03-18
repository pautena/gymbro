import { Button, Grid2, TextField } from '@mui/material'
import { HeaderLayout, useNotificationCenter } from '@pautena/react-design-system'
import { createFileRoute } from '@tanstack/react-router'
import { ApiError, WorkoutCreate, WorkoutsService } from '../../client'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { EventHandler, FormEvent } from 'react'

export const Route = createFileRoute('/_layout/workouts/add')({
  component: AddWorkout,
})

function AddWorkout() {
  const queryClient = useQueryClient()
  const { show } = useNotificationCenter()

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
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["workouts"] })
    },
  })

  const handleSubmit = (e:FormEvent) => {
    e.preventDefault();
    const data = new FormData(e.target as HTMLFormElement)
    mutation.mutate({
      name:data.get('name') as string
    })
  }

  return <HeaderLayout title="Add workout">
    <Grid2 container spacing={2} component="form" onSubmit={handleSubmit}>
        <Grid2 size={12}>
          <TextField
            name="name"
            label="Name"
            fullWidth
            required
            variant="outlined"
          />
        </Grid2>
        <Grid2 size={12}>
          <Button type='submit' variant='contained'>Save</Button>
      </Grid2>
    </Grid2>
  </HeaderLayout>
}
