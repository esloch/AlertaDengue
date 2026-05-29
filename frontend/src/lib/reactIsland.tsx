import type { ReactNode } from "react";
import { createRoot, type Root } from "react-dom/client";

type ReactIslandOptions<Props> = {
  rootId: string;
  propsId: string;
  render: (props: Props) => ReactNode;
};

export function mountReactIsland<Props>({
  rootId,
  propsId,
  render,
}: ReactIslandOptions<Props>): Root | null {
  const rootElement = document.getElementById(rootId);
  const propsElement = document.getElementById(propsId);

  if (!rootElement || !propsElement?.textContent) {
    return null;
  }

  const props = JSON.parse(propsElement.textContent) as Props;
  const root = createRoot(rootElement);
  root.render(render(props));

  return root;
}
