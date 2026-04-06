from __future__ import annotations


class _DummyShader:
    def __init__(self) -> None:
        self.float_values: dict[str, float] = {}
        self.float_history: list[tuple[str, float]] = []

    def use(self) -> None:
        return

    def set_matrix4(self, _name: str, _value) -> None:
        return

    def set_float(self, name: str, value: float) -> None:
        self.float_values[name] = value
        self.float_history.append((name, value))


class _DummyTexture:
    def __init__(self, *, blend_mode: int, alpha_cutoff: float, has_alpha: bool) -> None:
        self.blend_mode: int = blend_mode
        self.alpha_cutoff: float = alpha_cutoff
        self.has_alpha: bool = has_alpha

    def use(self) -> None:
        return


class _DummyScene:
    def __init__(self, diffuse: _DummyTexture) -> None:
        self._diffuse: _DummyTexture = diffuse
        self._lightmap: _DummyTexture = _DummyTexture(blend_mode=0, alpha_cutoff=0.0, has_alpha=False)

    def texture(self, name: str, *, lightmap: bool = False):
        _ = name
        return self._lightmap if lightmap else self._diffuse


def _build_mesh(diffuse: _DummyTexture):
    from pykotor.gl.models import mdl

    mesh = mdl.Mesh.__new__(mdl.Mesh)
    mesh._scene = _DummyScene(diffuse)
    mesh.texture = "diffuse"
    mesh.lightmap = "NULL"
    mesh._vao = 1
    mesh._face_count = 3
    return mesh


def test_default_alpha_texture_renders_opaque(monkeypatch):
    from pykotor.gl.models import mdl

    calls: list[tuple[str, object]] = []
    monkeypatch.setattr(mdl, "HAS_PYOPENGL", True)
    monkeypatch.setattr(mdl, "glEnable", lambda value: calls.append(("enable", value)))
    monkeypatch.setattr(mdl, "glDisable", lambda value: calls.append(("disable", value)))
    monkeypatch.setattr(mdl, "glBlendFunc", lambda src, dst: calls.append(("blend", (src, dst))))
    monkeypatch.setattr(mdl, "glDepthMask", lambda value: calls.append(("depth", value)))
    monkeypatch.setattr(mdl, "glActiveTexture", lambda value: calls.append(("active", value)))
    monkeypatch.setattr(mdl, "glBindVertexArray", lambda value: calls.append(("vao", value)))
    monkeypatch.setattr(mdl, "glDrawElements", lambda *_args: calls.append(("draw", None)))

    shader = _DummyShader()
    diffuse = _DummyTexture(blend_mode=0, alpha_cutoff=0.0, has_alpha=True)
    mesh = _build_mesh(diffuse)

    mesh.draw(shader, object())

    assert ("disable", mdl.GL_BLEND) in calls
    assert ("alphaCutoff", 0.0) in shader.float_history
    assert shader.float_values["alphaCutoff"] == 0.0


def test_cutout_texture_disables_regular_blending(monkeypatch):
    from pykotor.gl.models import mdl

    calls: list[tuple[str, object]] = []
    monkeypatch.setattr(mdl, "HAS_PYOPENGL", True)
    monkeypatch.setattr(mdl, "glEnable", lambda value: calls.append(("enable", value)))
    monkeypatch.setattr(mdl, "glDisable", lambda value: calls.append(("disable", value)))
    monkeypatch.setattr(mdl, "glBlendFunc", lambda src, dst: calls.append(("blend", (src, dst))))
    monkeypatch.setattr(mdl, "glDepthMask", lambda value: calls.append(("depth", value)))
    monkeypatch.setattr(mdl, "glActiveTexture", lambda value: calls.append(("active", value)))
    monkeypatch.setattr(mdl, "glBindVertexArray", lambda value: calls.append(("vao", value)))
    monkeypatch.setattr(mdl, "glDrawElements", lambda *_args: calls.append(("draw", None)))

    shader = _DummyShader()
    diffuse = _DummyTexture(blend_mode=0, alpha_cutoff=0.01, has_alpha=True)
    mesh = _build_mesh(diffuse)

    mesh.draw(shader, object())

    assert ("disable", mdl.GL_BLEND) in calls
    assert ("alphaCutoff", 0.01) in shader.float_history
    assert shader.float_values["alphaCutoff"] == 0.0
    assert any(name == "enable" and value == mdl.GL_BLEND for name, value in calls)
