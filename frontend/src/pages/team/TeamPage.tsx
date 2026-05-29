import type {
  LinkListItem,
  TeamMember,
  TeamPageProps,
  TeamSection,
} from "./types";

function initials(name: string): string {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

function TeamMemberCard({ member }: { member: TeamMember }) {
  const name = member.href ? (
    <a className="team-name" href={member.href}>
      {member.name}
    </a>
  ) : (
    <span className="team-name">{member.name}</span>
  );

  return (
    <article className="team-card">
      <div className="team-person">
        <div className="team-photo">
          {member.photo ? (
            <img src={member.photo} alt={member.name} />
          ) : (
            <span aria-hidden="true">{initials(member.name)}</span>
          )}
        </div>
        {name}
      </div>
      <p className="team-role">{member.role}</p>
    </article>
  );
}

function LinkList({ items }: { items: LinkListItem[] }) {
  return (
    <>
      {items.map((item) => (
        <li key={`${item.label}-${item.href ?? item.text ?? ""}`}>
          {item.href ? (
            <a href={item.href} target="_blank" rel="noopener noreferrer">
              {item.label}
            </a>
          ) : (
            item.label
          )}
          {item.text ? ` - ${item.text}` : null}
          {item.children?.length ? (
            <ul>
              <LinkList items={item.children} />
            </ul>
          ) : null}
        </li>
      ))}
    </>
  );
}

function TeamSectionView({ section }: { section: TeamSection }) {
  if (section.kind === "members") {
    return (
      <section className="team-section">
        <h5 className="team-section-title">{section.title}</h5>
        <div className="team-grid">
          {section.members.map((member) => (
            <TeamMemberCard key={member.name} member={member} />
          ))}
        </div>
      </section>
    );
  }

  return (
    <section className="team-section">
      <h5 className="team-section-title">{section.title}</h5>
      <div className="team-list-card">
        {section.intro ? <p>{section.intro}</p> : null}
        <ul className={section.listClassName}>
          <LinkList items={section.items} />
        </ul>
      </div>
    </section>
  );
}

export function TeamPage({ hero, sections, contact }: TeamPageProps) {
  return (
    <div className="team-page">
      <section className="team-hero">
        <h4>{hero.title}</h4>
        <p>{hero.body}</p>
      </section>

      {sections.map((section) => (
        <TeamSectionView key={section.title} section={section} />
      ))}

      <p className="team-contact">
        <strong>{contact.prompt}</strong>{" "}
        <a href={contact.href}>{contact.label}</a>.
      </p>
    </div>
  );
}
