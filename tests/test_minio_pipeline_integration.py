from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
import yaml


COMPOSE = Path('containers/compose-minio.yaml')


def test_minio_services_join_existing_infodengue_network() -> None:
    """The S3 service and both helpers resolve on the existing network."""
    services = yaml.safe_load(COMPOSE.read_text())['services']
    for name in ('minio', 'minio-init', 'minio-materializer'):
        assert 'infodengue' in services[name]['networks']


@pytest.mark.parametrize(
    ('exclude', 'expected'),
    [
        ('', ['mirror', '--watch', 'miniostore/sinan-infodengue', '/incoming']),
        (
            'approved-fixtures/*',
            [
                'mirror',
                '--watch',
                '--exclude',
                'approved-fixtures/*',
                'miniostore/sinan-infodengue',
                '/incoming',
            ],
        ),
    ],
)
def test_legacy_mirror_exclusion_is_optional_and_shell_quoted(
    tmp_path: Path, exclude: str, expected: list[str]
) -> None:
    """Empty config preserves the old call; configured pattern is one arg."""
    service = yaml.safe_load(COMPOSE.read_text())['services'][
        'minio-materializer'
    ]
    command = service['command'][0].replace('/usr/bin/mc', 'mc').replace(
        '$$', '$'
    )
    capture = tmp_path / 'argv.json'
    fake_mc = tmp_path / 'mc'
    fake_mc.write_text(
        '#!/bin/sh\nprintf \'%s\\n\' "$@" > "$CAPTURE"\n'
    )
    fake_mc.chmod(0o755)
    env = {
        **os.environ,
        'PATH': f'{tmp_path}{os.pathsep}{os.environ["PATH"]}',
        'CAPTURE': str(capture),
        'MINIO_ROOT_USER': 'test-user',
        'MINIO_ROOT_PASSWORD': 'test-password',
        'MINIO_MATERIALIZER_EXCLUDE': exclude,
    }
    subprocess.run(['/bin/sh', '-c', command], env=env, check=True, capture_output=True)
    assert capture.read_text().splitlines() == expected


def test_compose_keeps_exclusion_empty_by_default() -> None:
    """The opt-in setting has an empty nonsecret default."""
    service = yaml.safe_load(COMPOSE.read_text())['services'][
        'minio-materializer'
    ]
    assert service['environment']['MINIO_MATERIALIZER_EXCLUDE'] == (
        '${MINIO_MATERIALIZER_EXCLUDE:-}'
    )
    assert service['volumes'][0] == '${DOCKER_HOST_INCOMING_DIR}:/incoming'


def test_materializer_exclusion_env_template_renders_empty_or_configured() -> None:
    """The tracked env template preserves unset and configured deployments."""
    template = Path('.envs/.env.tpl').read_text()
    assignment = 'MINIO_MATERIALIZER_EXCLUDE=${MINIO_MATERIALIZER_EXCLUDE}'
    assert (
        '# Optional in staging only: MINIO_MATERIALIZER_EXCLUDE=approved-fixtures/*'
        in template
    )
    assert assignment in template

    empty_env = {
        key: value
        for key, value in os.environ.items()
        if key != 'MINIO_MATERIALIZER_EXCLUDE'
    }
    empty = subprocess.run(
        ['/usr/bin/envsubst'], input=assignment + '\n', text=True,
        capture_output=True, check=True, env=empty_env,
    )
    configured = subprocess.run(
        ['/usr/bin/envsubst'], input=assignment + '\n', text=True,
        capture_output=True, check=True,
        env={**empty_env, 'MINIO_MATERIALIZER_EXCLUDE': 'approved-fixtures/*'},
    )
    assert empty.stdout == 'MINIO_MATERIALIZER_EXCLUDE=\n'
    assert configured.stdout == 'MINIO_MATERIALIZER_EXCLUDE=approved-fixtures/*\n'
