export type TeamMember = {
  name: string;
  role: string;
  href?: string;
  photo?: string;
};

export type LinkListItem = {
  label: string;
  href?: string;
  text?: string;
  children?: LinkListItem[];
};

export type TeamSection =
  | {
      kind: "members";
      title: string;
      members: TeamMember[];
    }
  | {
      kind: "list";
      title: string;
      intro?: string;
      listClassName?: string;
      items: LinkListItem[];
    };

export type TeamPageProps = {
  hero: {
    title: string;
    body: string;
  };
  sections: TeamSection[];
  contact: {
    prompt: string;
    label: string;
    href: string;
  };
};
