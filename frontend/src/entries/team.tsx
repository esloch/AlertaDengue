import { mountReactIsland } from "../lib/reactIsland";
import { TeamPage } from "../pages/team/TeamPage";
import type { TeamPageProps } from "../pages/team/types";
import "../styles/team.css";

mountReactIsland<TeamPageProps>({
  rootId: "team-react-root",
  propsId: "team-page-props",
  render: (props) => <TeamPage {...props} />,
});
