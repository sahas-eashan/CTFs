FROM ubuntu:24.04 AS chroot

RUN /usr/sbin/useradd --no-create-home user

COPY flag /
COPY chal log /home/user/
RUN chmod +x /home/user/chal /home/user/log

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD /home/user/log

