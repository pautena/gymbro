import DashboardIcon from "@mui/icons-material/Dashboard"
import FitnessCenterIcon from "@mui/icons-material/FitnessCenter"
import ListIcon from "@mui/icons-material/List"
import type { DrawerNavigation } from "@pautena/react-design-system"

export function useGetSidebarNav(): DrawerNavigation {
  return [
    {
      id: "dashboard",
      kind: "link",
      text: "Dashboard",
      icon: <DashboardIcon />,
      href: "/",
    },
    {
      id: "items",
      kind: "link",
      text: "Items",
      icon: <ListIcon />,
      href: "/items",
    },
    {
      id: "workouts",
      kind: "link",
      text: "Workouts",
      icon: <FitnessCenterIcon />,
      href: "/workouts",
    },
  ]
}
